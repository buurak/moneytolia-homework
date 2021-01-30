from app import db


class Dashboard(db.Model):
    __table_args__ = {'extend_existing': True} 
    points = db.Column(db.Integer())
    wordlist = db.Column(db.PickleType())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    def __init__(self, points, wordlist):
        self.points = points
        self.wordlist = wordlist

    def __repr__(self):
        return "<Dashboard %r>" % (self.user_id)
