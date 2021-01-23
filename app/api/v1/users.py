from flask import jsonify, request, url_for, current_app
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask.views import MethodView
from . import v1
from app.models import User, Post, Comment


class UserAPIMethodView(MethodView):

    def get(self, user_id: int = None, slug=None):
        if user_id is None:
            return jsonify({'data': [user.api_to_json() for user in User.query.all()]})

        else:
            return jsonify({'data': User.query.get_or_404(int(user_id)).api_to_json()})

    def post(self):
        user = User(
            username=request['username'],
            email=request['email'],
            password=str(generate_password_hash(request['password'])),
            name=request['name'],
            address=request['address'],
        )

        db.session.add(user)
        db.session.commit()

        return jsonify(user.api_to_json())

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        name = request['name']
        address = request['address']
        db.session.commit()

        return jsonify(user.api_to_json())


user_view = UserAPIMethodView.as_view('user_api')
v1.add_url_rule(
    '/users', defaults={'user_id': None}, view_func=user_view, methods=['GET', ])
v1.add_url_rule('/users', view_func=user_view, methods=['POST'])
v1.add_url_rule('/users/<int:user_id>', view_func=user_view,
                methods=['GET', 'PUT', 'PATCH', 'DELETE'])


@v1.route("/users/<slug>", methods=['GET'])
def user_for_slug(slug=None):
    return jsonify({'data': User.query.filter_by(slug=slug).first().api_to_json()})


@v1.route('/users/<int:user_id>/posts', methods=['GET', ])
def user_posts(user_id: int = None):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(user_id=user_id).paginate(
        page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
    posts = pagination.items

    prev = None
    if prev:
        prev = url_for('v1.user_posts', user_id=user_id,
                       page=page-1, _external=True)

    next = None
    if next:
        next = url_for('v1.user_posts', user_id=user_id,
                       page=page+1, _external=True)

    return jsonify({'data': [post.to_json() for post in posts], 'links': {'prev': prev, 'next': next}, 'count': pagination.total})


@v1.route('/users/<slug>/posts', methods=['GET', ])
def user_posts_slug(slug=None):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(slug=slug).first()
    pagination = Post.query.filter_by(user_id=user.id).paginate(
        page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
    posts = pagination.items

    prev = None
    if prev:
        prev = url_for('v1.user_posts_slug', slug=slug,
                       page=page-1, _external=True)

    next = None
    if next:
        next = url_for('v1.user_posts_slug', slug=slug,
                       page=page+1, _external=True)

    return jsonify({'data': [post.to_json() for post in posts], 'links': {'prev': prev, 'next': next}, 'count': pagination.total})


@v1.route('/users/<int:user_id>/posts/<int:post_id>', methods=['GET', ])
def user_post(user_id=None, post_id=None):

    post = Post.query.filter_by(user_id=user_id).first()

    return jsonify({'data': post.to_json()})


@v1.route('/users/<int:user_id>/comments', methods=['GET', ])
def user_comments(user_id=None):
    page = request.args.get('page', 1, type=int)
    pagination = None

    pagination = Comment.query.filter_by(user_id=user_id).paginate(
        page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)

    comments = pagination.items

    prev = None
    if prev:
        prev = url_for('v1.user_comments', user_id=user_id,
                       page=page-1, _external=True)

    next = None
    if next:
        next = url_for('v1.user_comments', user_id=user_id,
                       page=page+1, _external=True)
    return jsonify({'data': [comment.to_json() for comment in comments], 'links': {'prev': prev, 'next': next}, 'count': pagination.total})


@v1.route('/users/<int:user_id>/comments/<int:comment_id>', methods=['GET', ])
def user_comment(user_id=None, comment_id=None):
    comment = Comment.query.filter_by(user_id=user_id).first()

    return jsonify({'data': comment.to_json()})
