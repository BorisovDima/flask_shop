from functools import wraps

from flask_login import current_user
from flask import redirect, url_for


def not_login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        else:
            return view(*args, **kwargs)
    return inner