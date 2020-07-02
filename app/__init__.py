from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_pagedown import PageDown
from config import os, config, BASE_DIR

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message_category = 'success'
login_manager.login_view = 'users.login'
pagedown = PageDown()
migrate = Migrate()

def create_app(config_name):
	app = Flask(__name__ ,
		instance_relative_config=True,
		template_folder=os.path.join(BASE_DIR,'html/templates'),
		static_folder=os.path.join(BASE_DIR,'html/static')
	)
	app.config.from_object(config.get(config_name))
	config[config_name].init_app(app)

	csrf.init_app(app)
	login_manager.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)
	migrate.init_app(app, db)

	from app.main import main
	app.register_blueprint(main)

	from app.users import users
	app.register_blueprint(users)

	from app.posts import posts
	app.register_blueprint(posts)

	from app.admin import admin
	app.register_blueprint(admin, url_prefix = '/admin')

	from app.api.v1 import v1 as api_v_1
	app.register_blueprint(api_v_1, url_prefix = '/api/v1')

	return app