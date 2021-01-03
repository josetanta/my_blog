import os
from config import config, BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_pagedown import PageDown
from app.helpers import isActive, momentjs

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message_category = 'success'
login_manager.login_view = 'users.login'
pagedown = PageDown()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder=os.path.join(BASE_DIR, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static')
                )
    app.config.from_object(config.get(config_name))
    config[config_name].init_app(app)

    # Variables goblas
    app.jinja_env.globals['momentjs'] = momentjs
    app.jinja_env.globals['isActive'] = isActive

    csrf.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    pagedown.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .users import users
    app.register_blueprint(users)

    from .posts import posts
    app.register_blueprint(posts)

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .api.v1 import v1 as api_v_1
    app.register_blueprint(api_v_1, url_prefix='/api/v1')

    return app
