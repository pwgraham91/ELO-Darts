import sqlalchemy

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)

    elo = db.Column(db.Float, default=10.0)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    deleted_at = db.Column(db.DateTime)

    winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    loser_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    submitted_by = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))
