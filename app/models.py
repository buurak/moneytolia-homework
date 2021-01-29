from app import db
from app import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50),nullable=False)
    dashboard = db.relationship('Dashboard', backref='user', uselist=False)

    def __repr__(self):
        return self.username

class Dashboard(db.Model):
    wordlist = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeingKey('user.id'))