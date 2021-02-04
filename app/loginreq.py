from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash('Please login to see this page!', 'danger')
            return redirect(url_for('user.login'))

    return decorated_function