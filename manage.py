import os
from dotenv import load_dotenv
from app.models import User, Post, Role, Follow, Comment
from flask_migrate import MigrateCommand, upgrade
from flask_script import Manager, Shell, Server
from app import create_app, db, migrate

load_dotenv(verbose=True)

app = create_app(os.getenv('FLASK_ENV') or 'default')
manager = Manager(app)
server = Server(port=os.getenv('FLASK_RUN_PORT'))


def shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Role=Role, Follow=Follow, Comment=Comment)


manager.add_command('shell', Shell(make_context=shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', server)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command("test")
def test_flask():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def seed():
    """
    Ejecuta el seed.py, creación de factories `create_user()`
    """

    from app.seed import create_users

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
