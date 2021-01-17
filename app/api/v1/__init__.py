from flask import Blueprint

v1 = Blueprint('v1', __name__)

from . import users, posts, comments
