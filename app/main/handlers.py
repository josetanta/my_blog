from flask import render_template, flash
from . import main

@main.app_errorhandler(404)
def get_404(e):
	flash(f'Esta url no existe.', 'danger')
	return render_template('handlers/404.html', title = 'Error de 404'), 404

@main.app_errorhandler(403)
def get_403(e):
	flash(f'No tienes permisos necesarios para porder acceder.', 'warning')
	return render_template('handlers/403.html', title='Error de 403'), 403

@main.app_errorhandler(405)
def get_405(e):
	flash(f'De momento esta URL, no esta disponible.', 'info')
	return render_template('handlers/405.html', title='Error de 405'), 405

@main.app_errorhandler(500)
def get_500(e):
	flash(f'Error en el servidor', 'danger')
	return render_template('handlers/500.html', title='Error de 500'), 500