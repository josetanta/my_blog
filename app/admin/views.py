from flask import render_template, redirect, url_for
from . import admin
from flask_login import login_required
from ..decorators import admin_required
from ..models import Post, User, db, Role, Comment


@admin.route('/')
@admin.route('/posts/', methods=['GET'])
@login_required
@admin_required
def posts():
    posts = Post.query.order_by(Post.date_register.desc())
    return render_template('admin/posts.html', title='Admin | Posts', posts=posts)


@admin.route('/comments/', methods=['GET'])
@login_required
@admin_required
def comments():
    comments = Comment.query.order_by(Comment.timestamp.desc())
    return render_template('admin/comments.html', title='Admin | Comments', comments=comments)


@admin.route('/users/', methods=['GET'])
@login_required
@admin_required
def users():
    role = Role.query.filter_by(name='User').first()
    users = role.users

    return render_template('admin/users.html', title='Admin | Users', users=users)


@admin.route('/users/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def show_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', title=user.username, user=user)


@admin.route('/status_post/<int:post_id>', methods=['GET'])
@login_required
@admin_required
def ban_post(post_id: int):
    """
    Método para restringir la visibilidad de una publicación
    """
    post = Post.query.get_or_404(post_id)
    if post.publishied:
        post.publishied = False
    else:
        post.publishied = True
    db.session.commit()
    return post.get_id()


@admin.route('/status_comment/<int:comment_id>', methods=['GET'])
@login_required
@admin_required
def ban_comment(comment_id: int) -> int:
    """
    Método para restringir la visibilidad de un comentario
    """
    coment = Comment.query.get_or_404(comment_id)
    if coment.publishied:
        coment.publishied = False
    else:
        coment.publishied = True
    db.session.commit()
    return coment.get_id()
