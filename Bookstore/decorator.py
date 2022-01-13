from functools import wraps
from flask import session, request, redirect, url_for
from flask_login import current_user
from Bookstore.models import UserRole


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/admin')

        return f(*args, **kwargs)

    return decorated_function


def manage_permission_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if current_user.user_role == UserRole.ADMIN:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return check
