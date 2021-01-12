from flask import Blueprint, current_app
from app.models import Permission
from . import forms
main = Blueprint('main', __name__)

from .views import *
from .handlers import *

@main.app_context_processor
def inject_permissions():
    return dict(
        Permission=Permission,
        form_send=forms.SendEmailForm()
    )
