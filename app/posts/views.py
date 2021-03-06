import os
from . import posts
from .forms import PostCreateForm, CommentForm
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    abort
)
from flask_login import current_user, login_required
from ..models import Post, Permission, Comment
from ..decorators import permission_required
from .. import db
from ..utils import save_upload


@posts.route('/post/<slug>', methods=['GET', 'POST', 'PUT'])
def post_show(slug):
    """
    View for create new post and update
    """
    post = Post.query.filter_by(slug=slug).first()

    form = PostCreateForm()
    try:
        if current_user == post.author:
            if form.validate_on_submit():

                # Traer el path del upload Post
                image_current_del = os.path.join(
                    current_app.root_path, "static/uploads/posts", post.upload)

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
                form.url_image.data = post.url_image
    except AttributeError:
        raise abort(404)

    c_form = CommentForm()
    comments_of_post = db.session.query(Comment).join(Post).filter(
        Comment.post_id == post.id).order_by(db.desc(Comment.timestamp)).all()
    return render_template('posts/show.html', title=f'Post {post.title}', post=post, form=form, c_form=c_form, comments_of_post=comments_of_post)


@posts.route('/posts/<slug>', methods=['POST', 'DELETE'])
@login_required
@permission_required(Permission.WRITE_POST)
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
            url_image=form.url_image.data,
        )
        # Pregunstar si existe un archivo en el input(esto desde el request)
        if request.files['upload']:
            # Crear un nuevo upload para el post
            img = save_upload(form.upload.data, model='posts')

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
def comment(slug: str):
    c_form = CommentForm()
    post = Post.query.filter_by(slug=slug).first()
    if current_user.is_authenticated and c_form.validate_on_submit():
        comment = Comment(body=c_form.body.data, post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Se publico su comentario.', 'success')
        return redirect(url_for('.post_show', slug=post.slug))

    else:
        flash('Por favor el comentario debe tener más de 20 caracteres.', 'danger')
        return redirect(url_for('.post_show', slug=post.slug))


@posts.route('/posts/<slug>/comments/<comment_id>', methods=['DELETE', 'POST'])
@login_required
def comment_delete(slug=None, comment_id=None):
    post = Post.query.filter_by(slug=slug).first()
    comment = Comment.query.filter_by(post=post).first()

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.post', slug=post.slug))
