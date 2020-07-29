import os
from . import posts
from .forms import PostCreateForm, CommentForm
from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_required
from app.models import Post, User, Permission, Comment
from app.decorators import permission_required
from app import db
from app.utils import save_upload


@posts.route('/post/<slug>', methods=['GET', 'POST', 'PUT'])
def post(slug):
    post = Post.query.filter_by(slug=slug).first()

    form = PostCreateForm()
    if current_user == post.author:
        if form.validate_on_submit():

            # Traer el path del upload Post
            image_current_del = os.path.join(
                current_app.root_path, "html\\static\\uploads\\posts", post.upload)

            if request.files['upload']:

                if os.path.exists(image_current_del):
                    # Eliminar el upload actual
                    os.remove(image_current_del)

                # Actualizar el nuevo file subido.
                img = save_upload(form.upload.data, 'posts', 700)

                # Se asigna como nuevo upload al post
                post.upload = img

            post.title = form.title.data
            post.content = form.pagedown.data
            db.session.commit()
            flash(f'Actualizaste tu post {post.title}', 'success')
            return redirect(url_for('posts.post', slug=post.slug))
        else:
            form.title.data = post.title
            form.pagedown.data = post.content
            form.upload.data = post.upload

    c_form = CommentForm()

    return render_template('posts/show.html', title=f'Post {post.title}', post=post, form=form, c_form=c_form)


@posts.route('/posts/<slug>', methods=['POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def post_delete(slug):
    post = Post.query.filter_by(slug=slug).first()
    if current_user == post.author:
        db.session.delete(post)
        db.session.commit()
        flash('Usted ah confirmado la eliminación de su post', 'secondary')
    else:
        flash('Usted no tiene permiso para esta acción', 'warning')
    return redirect(url_for('main.home'))


@posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.WRITE_POST)
def new():
    form = PostCreateForm()
    if current_user.can(Permission.WRITE_POST) and form.validate_on_submit():
        new_post = Post(
            title=form.title.data.strip(),
            content=form.pagedown.data,
            author=current_user._get_current_object(),
        )
        # Pregunstar si existe un archivo en el input(esto desde el request)
        if request.files['upload']:
            # Crear un nuevo upload para el post
            img = save_upload(form.upload.data)

            # Se asigna como nuevo upload al post
            new_post.upload = img

        db.session.add(new_post)
        db.session.commit()
        flash(f'Se creo tu post "{form.title.data}"', 'success')
        return redirect(url_for('main.home'))

    return render_template('posts/new.html', title='Crear Post', Permission=Permission, form=form)


@posts.route('/posts/<slug>/comments', methods=['POST'])
@login_required
@permission_required(Permission.COMMENT)
def comment(slug):
    c_form = CommentForm()
    if current_user.is_authenticated and c_form.validate_on_submit():
        post = Post.query.filter_by(slug=slug).first()
        comment = Comment(body=c_form.body.data, post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Se publico su comentario.', 'success')
        return redirect(url_for('.post', slug=post.slug))


@posts.route('/posts/<slug>/comments/<id>', methods=['DELETE','POST'])
@login_required
def comment_delete(slug=None, id=None):
    post = Post.query.filter_by(slug=slug).first()
    comment = Comment.query.filter_by(post=post).first()

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.post', slug=post.slug))
