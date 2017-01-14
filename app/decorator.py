from functools import wraps
from flask import request, g, abort
from flask_login import current_user
from app.models import UserModel


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_administrator():
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator


def permission_required(f, permission):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.can(permission):
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator