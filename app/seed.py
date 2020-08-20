from .models import db, Role


def create_users():
    # Genera todos los roles de usuario
    Role.generate_roles()
    db.session.commit()
