from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/login')
def login():
    return 'Login Page'

@user.route('/signup')
def signup():
    return 'Register Page'
