from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

from app.models.models import User, Dashboard

from .user.routes import user
from .dashboard.routes import dashboard
from .words.routes import words

app.register_blueprint(user)
app.register_blueprint(dashboard)
app.register_blueprint(words)

db.create_all()