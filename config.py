import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_ENABLED = os.getenv('SECRET_KEY')
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_DB_QUERY_TIMEOUT = 0.5
    FLASK_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    EMAIL_BLOG_ADMIN = os.environ.get('MAIL_ADMIN')
    API_KEY = os.getenv('API_KEY_MAILGUN')
    API_URL = os.getenv('API_URL_MAILGUN')
    APP_NAME = os.getenv('APP_NAME')
    GITHUB = os.getenv('GITHUB')

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/site-dev.sqlite3'


class DevelopmentMySQl(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://adminblog:password@localhost/blogbd"


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/site-production.sqlite3'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class HerokuConfig(Production):

    @classmethod
    def init_app(cls, app):
        Production.init_app(app)

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class Test(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/site-test.sqlite3'


config: dict = {
    'development': Development,
    'developmentmysql': DevelopmentMySQl,
    'production': Production,
    'test': Test,
    'heroku': HerokuConfig,

    'default': Development,
}
