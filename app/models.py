import sqlalchemy

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())

    elo = db.Column(db.Float, default=100.0)
    wins = db.Column(db.Integer, default=0, nullable=False)
    losses = db.Column(db.Integer, default=0, nullable=False)

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

    @property
    def total_games(self):
        return self.wins + self.losses

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'admin': self.admin,
            'avatar': self.avatar,
            'active': self.active,
            'created_at': self.created_at.strftime('%b %d %Y %I:%M%p'),
            'elo': self.elo,
            'wins': self.wins,
            'losses': self.losses
        }


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    deleted_at = db.Column(db.DateTime)

    winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    winner_elo_score = db.Column(db.Float, nullable=False)
    loser_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    loser_elo_score = db.Column(db.Float, nullable=False)
    submitted_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))

    winner = db.relationship("User", foreign_keys=[winner_id], backref=sqlalchemy.orm.backref('winners'))
    loser = db.relationship("User", foreign_keys=[loser_id], backref=sqlalchemy.orm.backref('losers'))
    submitted_by = db.relationship("User", foreign_keys=[submitted_by_id], backref=sqlalchemy.orm.backref('submitters'))

    @property
    def dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%b %d %Y %I:%M%p'),
            'deleted_at': self.deleted_at.strftime('%b %d %Y %I:%M%p') if self.deleted_at else None,
            'winner_id': self.winner_id,
            'winner_elo_score': self.winner_elo_score,
            'loser_id': self.loser_id,
            'loser_elo_score': self.loser_elo_score,
            'submitted_by_id': self.submitted_by_id,
        }
