from flask import render_template, redirect, url_for
from app.admin import admin
from flask_login import login_required
from app.decorators import admin_required
from app.models import Post, User, db, Role

@admin.route('/')
@login_required
@admin_required
def index():
	return render_template('admin/index.html', title = 'Dashboard')

@admin.route('/status_post/<int:id>', methods=['GET'])
@login_required
@admin_required
def ban(id):
	post = Post.query.get_or_404(id)
	if post.status:
		post.status = False
	else:
		post.status = True
	db.session.commit()
	return post.get_id()


@admin.route('/posts/',methods = ['GET'])
@login_required
@admin_required
def posts():
	posts = Post.query.order_by(Post.date_register.desc())
	posts_pub = list(filter(lambda p: p.status == True, posts))
	posts_ban = list(filter(lambda p: p.status == False, posts))
	return render_template('admin/posts.html', title = 'Admin | Posts', posts_pub = posts_pub, posts_ban = posts_ban, posts = posts)

@admin.route('/comments/',methods = ['GET'])
@login_required
@admin_required
def comments():
	return render_template('admin/comments.html', title = 'Admin | Comments')

@admin.route('/users/',methods = ['GET'])
@login_required
@admin_required
def users():
	role = Role.query.filter_by(name = 'User').first();
	users = role.users;

	return render_template('admin/users.html', title = 'Admin | Users', users = users)

@admin.route('/users/<int:id>', methods = ['GET'])
@login_required
@admin_required
def show_user(id):
	user = User.query.get_or_404(id)
	return render_template('users/show.html', title = user.username, user = user)