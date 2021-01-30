from flask import Blueprint

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/<int:id>')
def user_dashboard(id):
    return 'dashboard'