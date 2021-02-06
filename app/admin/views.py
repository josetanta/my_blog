from flask import render_template, redirect, url_for
from . import admin
from flask_login import login_required
from ..decorators import admin_required
from ..models import Post, User, db, Role, Comment


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html', title='Dashboard')


@admin.route('/status_post/<int:post_id>', methods=['GET'])
@login_required
@admin_required
def ban(post_id):
    post = Post.query.get_or_404(post_id)
    if post.status:
        post.status = False
    else:
        post.status = True
    db.session.commit()
    return post.get_id()


@admin.route('/posts/', methods=['GET'])
@login_required
@admin_required
def posts():
    posts = Post.query.order_by(Post.date_register.desc())
    posts_pub = list(filter(lambda p: p.status == True, posts))
    posts_ban = list(filter(lambda p: p.status == False, posts))
    return render_template('admin/posts.html', title='Admin | Posts', posts_pub=posts_pub, posts_ban=posts_ban,
                           posts=posts)


@admin.route('/comments/', methods=['GET'])
@login_required
@admin_required
def comments():
    comments = Comment.query.all()
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
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', title=user.username, user=user)
