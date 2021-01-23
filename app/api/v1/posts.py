from ... import db
from flask import jsonify, request, current_app, url_for
from flask.views import MethodView
from . import v1
from ...models import Post, Comment


class PostAPIMethodView(MethodView):

    def get(self, post_id=None, slug=None):

        if post_id:
            return jsonify({'data': Post.query.get_or_404(post_id).to_json()})
        elif slug:
            return jsonify({'data': Post.query.filter_by(slug=slug).first().to_json()})
        else:
            page = request.args.get('page', 1, type=int)
            pagination = Post.query.paginate(
                page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
            posts = pagination.items

            prev = None
            if pagination.has_prev:
                prev = url_for('v1.post_api', page=page-1, _external=True)
            next = None
            if pagination.has_next:
                next = url_for('v1.post_api', page=page+1, _external=True)

            return jsonify({'data': [post.to_json() for post in posts],
                            'links': {
                'self': url_for('v1.post_api', _external=True), 'next': next, 'prev': prev}, 'count': pagination.total
            })

    def post(self):
        post = Post(
            title=request['title'],
            body=request['body'],
            author=request['author'],
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
        post.author = request['author']

        db.session.commit()

        return jsonify(post.to_json())


post_view = PostAPIMethodView.as_view('post_api')
v1.add_url_rule(
    '/posts', defaults={'post_id': None}, view_func=post_view, methods=['GET'])
v1.add_url_rule('/posts', view_func=post_view, methods=['POST'])
v1.add_url_rule('/posts/<int:post_id>', view_func=post_view,
                methods=['GET', 'PUT', 'DELETE', 'PATCH'])
v1.add_url_rule('/posts/<slug>', view_func=post_view,
                methods=['GET', 'PUT', 'DELETE', 'PATCH'])


@v1.route('/posts/<int:post_id>/comments', methods=['GET'])
def post_comments(post_id: int = None):
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(post_id=post_id).paginate(
        page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
    comments = pagination.items

    prev = None
    if prev:
        prev = url_for('v1.post_comments', post_id=post_id,
                       page=page-1, _external=True)

    next = None
    if next:
        next = url_for('v1.post_comments', post_id=post_id,
                       page=page+1, _external=True)

    return jsonify({'data': [comment.to_json() for comment in comments], 'links': {'next': next, 'prev': prev}, 'count': pagination.total})


@v1.route('/posts/<slug>/comments', methods=['GET'])
def post_comments_slug(slug=None):
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter(Post.slug == slug).paginate(
        page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
    comments = pagination.items

    prev = None
    if prev:
        prev = url_for('v1.post_comments_slug', slug=slug,
                       page=page-1, _external=True)

    next = None
    if next:
        next = url_for('v1.post_comments_slug', slug=slug,
                       page=page+1, _external=True)

    return jsonify({'data': [comment.to_json() for comment in comments], 'links': {'next': next, 'prev': prev}, 'count': pagination.total})


@v1.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
def post_comment(post_id: int = None, comment_id=None):
    comment = Comment.query.filter_by(post_id=post_id).first()

    return jsonify({'data': comment.to_json()})
