from flask import Blueprint, current_app
from app.models import Permission
main = Blueprint('main', __name__)

from . import forms
from .views import *
from .handlers import *

@main.app_context_processor
def inject_permissions():
    return dict(
        Permission=Permission,
        form_send=forms.SendEmailForm()
    )
