# -*- encoding: utf-8 -*-
"""
Role-based access control decorators
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('authentication_blueprint.login'))

        if not current_user.is_admin():
            flash('You do not have permission to access this resource.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def lower_admin_required(f):
    """Decorator to require lower_admin or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('authentication_blueprint.login'))

        if not (current_user.is_admin() or current_user.is_lower_admin()):
            flash('You do not have permission to access this resource.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def firewall_access_required(f):
    """Decorator to require firewall module access (admin or lower_admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('authentication_blueprint.login'))

        if not (current_user.is_admin() or current_user.is_lower_admin()):
            flash('You do not have firewall access.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
