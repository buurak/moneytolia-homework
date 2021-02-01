from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    dashboard = db.relationship("Dashboard", backref="user", uselist=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % (self.id)


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points = db.Column(db.Integer,default=0)
    wordlist = db.Column(JSON)

    def __init__(self, user_id, wordlist):
        self.user_id = user_id
        self.wordlist = wordlist

    def __repr__(self):
        return "<Dashboard %r>" % (self.id)