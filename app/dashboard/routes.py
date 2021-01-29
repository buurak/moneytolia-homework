from flask import Blueprint

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/dashboard')
def user_dashboard():
    return 'dashboard'