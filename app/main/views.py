import asyncio
from flask import (
    render_template,
    flash,
    redirect,
    request,
    url_for,
    make_response,
    current_app,
    copy_current_request_context
)
from flask_login import current_user, login_required
from app.models import Post, db
from app.posts.forms import PostCreateForm
from flask_sqlalchemy import get_debug_queries
from . import main
from flask.views import MethodView
from .forms import SendEmailForm
from app.models import User
from app.mail import send_email_admin

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASK_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning('Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' % (
                query.statement, query.parameters, query.duration, query.context))
    return response


@main.route('/', methods=['GET', 'POST'])
def home():
    form_email = SendEmailForm()

    # Paginación de los objectos a renderizar
    page = request.args.get('page', 1, type=int)

    posts = Post.query.filter_by(status=True)\
        .order_by(Post.date_register.desc())\
        .paginate(page=page, per_page=4)
    return render_template('index.html', title='Home', posts=posts, form_email=form_email)


@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    form_email = SendEmailForm()
    r = request.form.to_dict()
    if current_user.is_authenticated and form_email.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        asyncio.run(send_email_admin(
            user, form_email.title.data, form_email.body.data))
        flash(f'Gracias por tu recomendación', 'success')
        return redirect(url_for('.home'))


@main.route('/about')
def about():
    return render_template('about.html', title='About')
