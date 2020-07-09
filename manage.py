from dotenv import load_dotenv
load_dotenv(verbose=True)

import os
from flask import current_app
from app import create_app, db, migrate
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, upgrade
from app.models import User, Post, Role, Follow, Comment

app = create_app(os.getenv('FLASK_ENV'))
print(os.getenv('FLASK_ENV'))
manager = Manager(app)


def shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Role=Role, Follow=Follow, Comment=Comment)


manager.add_command('shell', Shell(make_context=shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def seed():
    from app.seed import create_users
    """
	Ejecuta el seed.py, creación de factories
	"""
    create_users()


@manager.command
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.generate_roles()


if __name__ == '__main__':
    manager.run()
