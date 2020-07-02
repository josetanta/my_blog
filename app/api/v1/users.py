from flask import jsonify, request
from app import db
from werkzeug.security import generate_password_hash
from app.decorators import permission_api
from flask_login import login_required
from flask.views import MethodView
from . import v1
from app.models import User

class UserAPI(MethodView):

	decorators = [permission_api]

	def get(self, user_id):
		if user_id is None:
			users = User.query.all()
			return jsonify([user.api_to_json() for user in users])
		else:
			user = User.query.get_or_404(int(user_id))
			return jsonify(user.api_to_json())

	def post(self):
		user = User(
			username 	= request['username'],
			email 		= request['email'],
			password 	= str(generate_password_hash(request['password'])),
			name 		= request['name'],
			address 	= request['address'],

		)

		db.session.add(user)
		db.session.commit()

		return jsonify(user.api_to_json())

	def delete(self, user_id):
		user = User.query.get_or_404(user_id)
		db.session.delete(user)
		db.session.commit()

	def put(self, user_id):
		user		= User.query.get_or_404(user_id)
		name 		= request['name']
		address 	= request['address']
		db.session.commit()

		return jsonify(user.api_to_json())

user_view = UserAPI.as_view('user_api')
v1.add_url_rule('/users/', defaults={'user_id': None},view_func=user_view, methods=['GET',])
v1.add_url_rule('/users/',view_func=user_view, methods=['POST'])
v1.add_url_rule('/users/<int:user_id>', view_func=user_view,methods=['GET', 'PUT','PATCH','DELETE'])