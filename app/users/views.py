import os
import asyncio
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    make_response,
    session,
    current_app
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from .forms import (
    RegisterForm,
    LoginForm,
    AccountForm,
    EmailResetPasswordForm,
    ResetPasswordForm
)

from ..decorators import permission_required
from ..utils import save_upload
from ..models import User, db, Permission, Post
from ..mail import send_token_confirmation, send_token_reset_password
from ..main.forms import SendEmailForm
from . import users


@users.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'users' \
                and request.endpoint != 'static':
            return redirect(url_for('users.uncorfirmed'))


@users.route('/uncorfirmed')
def uncorfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('users/unconfirmed.html', title="Cuenta no confirmada")


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmed_token()
        asyncio.run(send_token_confirmation(user, token))
        flash(f'Te hemos enviado un mensaje de confirmación de cuenta a tu correo.', 'info')
        return redirect(url_for('main.home'))

    return render_template('users/register.html', form=form, title='Registrarse')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            session['email'] = form.email.data
            return redirect(url_for('main.home'))
        else:
            flash('Por favor vuelva a Ingresar su nombre de usuario y su contraseña correctamente, Gracias.', 'danger')

    return render_template('users/login.html', title='Iniciar Sesión', form=form)


@users.route('/logout')
@login_required
def logout():
    if 'username' in session:
        session.pop('username')
    flash('Cerraste tu Sesión', 'success')
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/auth/<slug>', methods=['GET'])
@users.route('/auth/<int:id>', methods=['GET'])
def show(slug: str = None):
    form_email = SendEmailForm()
    user = User.query.filter_by(slug=slug).first()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_register.desc())

    return render_template('users/show.html', title=user.username, user=user, posts=posts, form_email=form_email)


@users.route('/account/<slug>', methods=['POST', 'GET'])
@login_required
def account(slug=None, id=None):
    form = AccountForm()
    if form.validate_on_submit():

        # Traer el path del upload del usuario logueado (o en session)
        image_current_del = os.path.join(
            current_app.root_path, "static\\uploads\\users", current_user.upload)

        if request.files['upload']:

            # Eliminar el upload actual
            if os.path.exists(image_current_del):
                os.remove(image_current_del)

            # Actualizar el nuevo file subido(en este caso hizo un update el cliente)
            img = save_upload(form.upload.data, 'users')

            # Se asigna como nuevo upload al current user
            current_user.upload = img

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.address = form.address.data

        # Se guarda lo cambios
        db.session.commit()
        flash('Actualisaste tu cuenta.', 'success')
        return redirect(url_for('users.account', slug=current_user.slug))

    form.username.data = current_user.username
    form.email.data = current_user.email
    form.upload.data = current_user.upload
    form.name.data = current_user.name
    form.address.data = current_user.address

    return render_template('users/edit.html', title=f'{current_user.username}', form=form)


@users.route('/follow/<slug>', methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def follow(slug: str):
    user = User.query.filter_by(slug=slug).first()
    if current_user.is_authenticated:
        current_user.follow(user)
        return jsonify('following')


@users.route('/unfollow/<slug>', methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(slug: str):
    user = User.query.filter_by(slug=slug).first()
    if current_user.is_authenticated:
        current_user.unfollow(user)
        return jsonify('unfollowing')


@users.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    elif current_user.confirm(token):
        flash(
            f'Felicidades {current_user.username} te acabas de unir a nuestra comunidad', 'success')
    else:
        flash('La confirmación de cuenta a expirado', 'info')
    return redirect(url_for('main.home'))


@users.route('/confirm')
@login_required
def resend_cofirmation():
    token = current_user.generate_confirmed_token()
    asyncio.run(send_token_confirmation(current_user, token))
    flash('Se le envio a su correo un mensaje de confimación de cuenta', 'success')
    return redirect(url_for('main.home'))


@users.route('/reset-password', methods=['POST', 'GET'])
def send_token_reset_pass():
    email_form = EmailResetPasswordForm()

    if email_form.validate_on_submit():
        user = User.query.filter_by(email=email_form.email.data).first()
        token = user.get_reset_token()
        asyncio.run(send_token_reset_password(user, token))
        flash('Revise su correo por favor, se le envio una dirección para reestablecer su contraseña', 'info')
        return redirect(url_for('main.home'))

    return render_template('users/reset_password/send_email.html', title='Recuperar contraseña', email_form=email_form)


@users.route('/reset-password/<token>', methods=['POST', 'GET'])
def reset_password(token: str):
    form = ResetPasswordForm()
    user = User.verificar_reset_token(token=token)

    if user:
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.commit()
            flash('Ah reestablecido su contrseña correctamente', 'success')
            return redirect(url_for('users.login'))

    return render_template('users/reset_password/reset.html', title="Reestablecer su contraseña", form=form)
