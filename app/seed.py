from .models import User, Post, db, Role
from werkzeug.security import generate_password_hash


def create_users():
    # Genera todos los roles de usuario
    Role.generate_roles()

    db.session.commit()
