from app import db
from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required
from app.decorators import permission_api
from . import v1
from app.models import Post


class PostAPI(MethodView):
    decorators = [permission_api]

    def get(self, post_id):

        if post_id:
            return Post.query.get_or_404(post_id).to_json()
        else:
            return jsonify([post.to_json() for post in Post.query.all()])

    def post(self):
        post = Post(
            title=request['title'],
            body=request['body'],
            auth=request['auth'],
        )

        db.session.add(post)
        return jsonify(post.to_json())

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        post.title = request['title']
        post.body = request['body']
        post.auth = request['auth']

        db.session.commit()

        return jsonify(post.to_json())

post_view = PostAPI.as_view('post_api')
v1.add_url_rule(
    '/posts/', defaults={'post_id': None}, view_func=post_view, methods=['GET'])
v1.add_url_rule('/posts/', view_func=post_view, methods=['POST'])
v1.add_url_rule('/posts/<int:post_id>', view_func=post_view,
                methods=['GET', 'PUT', 'DELETE', 'PATCH'])
