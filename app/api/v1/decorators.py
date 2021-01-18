from functools import wraps
from flask import g
from .handlers import forbidden

def permission_required(f):
    @wraps(f)
    def _func_decorated(*args,**kwargs):
        if g.current_user.is_anonymous:
            return forbidden("No Authenticated")
        return f(*args, **kwargs)
    return _func_decorated
