from flask import current_app, url_for
import requests
from dotenv import load_dotenv
load_dotenv(verbose=True)


async def send_email_admin(user, title, body):
    msg = f'''
{body}
Perfil del Usuario: {url_for('admin.show_user', id = user.id, _external = True)}
'''
    send = requests.post(
        current_app.config['API_URL'],
        auth=("api", current_app.config['API_KEY']),
        data={
            "from": f"{user.username} <{user.email}>",
            "to": [f"{current_app.config['EMAIL_BLOG_ADMIN']}", f"{current_app.config['EMAIL_BLOG_ADMIN']}"],
            "subject": f"BlogJGTC - {title}",
            "text": msg,
        }
    )
    return send


async def send_token_confirmation(user, token):
    msg = f'''
Hola {user.username}.
Bienvenido al Blog (Comunidad)
Por favor dirigete a esta dirección de URL, para confirmar tu cuenta: {url_for('users.confirm', token = token, _external = True)}
Nota: No compartas con nadie este mensaje.
Atte: <Staff-Blog>
'''
    send = requests.post(
        current_app.config['API_URL'],
        auth=("api", current_app.config.get('API_KEY')),
        data={
            "from": f"BlogJGTC <{current_app.config.get('EMAIL_BLOG_ADMIN')}>",
            "to": [f"{user.username}", f"{user.email}"],
            "subject": "Confirmación de Cuenta de Blog",
            "text": msg,
        }
    )
    return send
