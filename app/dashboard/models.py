from app import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from app.user.models import User


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    wordlist = db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, points, wordlist):
        self.points = points
        self.wordlist = wordlist

    def __repr__(self):
        return "<Dashboard %r>" % (self.user_id)
