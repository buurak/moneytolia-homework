from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .user.routes import user
from .dashboard.routes import dashboard
from .words.routes import words

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'flaskloverburak'

app.register_blueprint(user)
app.register_blueprint(dashboard)
app.register_blueprint(words)



