from app import db
from sqlalchemy.dialects.postgresql import JSON


class Dashboard(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=True, primary_key=True
    )
    points = db.Column(db.Integer,default=0)
    wordlist = db.Column(JSON)

    def __init__(self, user_id, wordlist):
        self.user_id = user_id
        self.wordlist = wordlist

    def __repr__(self):
        return "<Dashboard %r>" % (self.user_id)
