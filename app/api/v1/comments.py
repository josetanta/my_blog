from flask import jsonify, request, current_app, url_for
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask.views import MethodView
from . import v1
from app.models import Comment


class CommentAPIMethodView(MethodView):

    def get(self, comment_id=None):
        if comment_id is None:
            page = request.args.get('page', 1, type=int)
            pagination = Comment.query.paginate(
                page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
            comments = pagination.items
            prev = None
            if pagination.has_prev:
                prev = url_for('v1.comment_api', page=page-1, _external=True)
            next = None
            if pagination.has_next:
                next = url_for('v1.comment_api', page=page+1, _external=True)

            return jsonify({'data': [comment.to_json() for comment in comments], 'links': {'next': next, 'prev': prev, 'self': url_for('v1.comment_api', _external=True)}, 'count': pagination.total})
        else:
            comment = Comment.query.get_or_404(int(comment_id))
            return jsonify({'data': comment.to_json()})

    def post(self):
        comment = Comment(
            body=request['body'],
            user_id=request['user_id'],
            post_id=request['post_id'],
            publishied=request['publishied']
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify(comment.to_json())

    def delete(self, comment_id: int):
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()

    def put(self, comment_id: int):
        comment = Comment.query.get_or_404(comment_id)
        body = request['body']
        publishied = request['publishied']
        db.session.commit()

        return jsonify(comment.to_json())


comment_view = CommentAPIMethodView.as_view('comment_api')
v1.add_url_rule('/comments', defaults={'comment_id': None},
                view_func=comment_view, methods=['GET', ])
v1.add_url_rule('/comments', view_func=comment_view, methods=['POST'])
v1.add_url_rule('/comments/<int:comment_id>', view_func=comment_view,
                methods=['GET', 'PUT', 'PATCH', 'DELETE'])
