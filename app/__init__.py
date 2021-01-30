from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'flaskloverburak'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/brk/Desktop/moneytolia-homework/words.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from .user.models import User
from .dashboard.models import Dashboard

from .user.routes import user
from .dashboard.routes import dashboard
from .words.routes import words

app.register_blueprint(user)
app.register_blueprint(dashboard)
app.register_blueprint(words)
