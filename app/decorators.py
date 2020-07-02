from functools import wraps
from flask import abort, flash
from flask_login import current_user
from app.models import Permission


# Permsisos requeridos para acciones de los usuarios
def permission_required(permission):
	"""
	Decorador para funciones de ejecución de permisos de pendiendo
	de los roles de cada usuario, para gestionar cada Post Publicado
	"""
	def _decorator(f):
		@wraps(f)
		def func_decorator(*args,**kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return func_decorator
	return _decorator

def admin_required(f):
	'''
	Permisos requeridos para acciones de rol de Administrador
	'''
	return permission_required(Permission.ADMINISTER)(f)


def permission_api(f):
	'''
	Acceso del Cliente a la API, debera tener los permisos
	necesesarios para poder visualizar la data
	'''
	return permission_required(Permission.PERMITE_API)(f)