from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .user.routes import user
from .dashboard.routes import dashboard

app = Flask(__name__)
db = SQLAlchemy(app)

def create_app():
    app.register_blueprint(user)
    app.register_blueprint(dashboard)

    return app
