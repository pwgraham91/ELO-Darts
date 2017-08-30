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
    average_elo = db.Column(db.Float, default=100.0)
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
            'losses': self.losses,
            'average_elo': self.average_elo
        }


class Game(db.Model):
    """ A `Game` is a whole match """
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, nullable=False, default=sqlalchemy.func.now())
    deleted_at = db.Column(db.DateTime)
    slack_user_submitted_by = db.Column(db.String(64))

    score_to_0 = db.Column(db.SmallInteger, nullable=False, default=201)
    double_out = db.Column(db.Boolean, nullable=False, default=False)
    rebuttal = db.Column(db.Boolean, nullable=False, default=True)
    best_of = db.Column(db.Integer, nullable=False, default=3)

    winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))
    # new elo score for the winner after the game has been played
    winner_elo_score = db.Column(db.Float)
    # average score of the winner after the game has been played
    winner_average_score = db.Column(db.Float)
    loser_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))
    # new elo score for the loser after the game has been played
    loser_elo_score = db.Column(db.Float)
    # average score of the loser after the game has been played
    loser_average_score = db.Column(db.Float)
    submitted_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))

    winner = db.relationship("User", foreign_keys=[winner_id], backref=sqlalchemy.orm.backref('winners'))
    loser = db.relationship("User", foreign_keys=[loser_id], backref=sqlalchemy.orm.backref('losers'))
    submitted_by = db.relationship("User", foreign_keys=[submitted_by_id], backref=sqlalchemy.orm.backref('submitters'))
    # keep track of who is playing the game
    in_progress_player_1_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))
    in_progress_player_2_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))

    in_progress_player_1 = db.relationship("User", foreign_keys=[in_progress_player_1_id],
                                           backref=sqlalchemy.orm.backref('in_progress_1'))
    in_progress_player_2 = db.relationship("User", foreign_keys=[in_progress_player_2_id],
                                           backref=sqlalchemy.orm.backref('in_progress_2'))


class Round(db.Model):
    """ a `Round` is a single game in a match. For example, if you're playing a 201 best out of 3, the 3 games are
        considered `Round`s and the whole match is a `Game`
    """

    id = db.Column(db.BigInteger, primary_key=True)

    game_id = db.Column(db.BigInteger, db.ForeignKey('game.id'), nullable=False)
    first_throw_player_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    round_winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    game = db.relationship("Game", backref="game_rounds")
    first_throw_player = db.relationship("User", foreign_keys=[first_throw_player_id],
                                         backref=sqlalchemy.orm.backref('first_throw_players'))
    round_winner = db.relationship("User", foreign_keys=[round_winner_id],
                                   backref=sqlalchemy.orm.backref('round_winner'))


class Throw(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hit_score = db.Column(db.Integer, nullable=False)
    hit_area = db.Column(db.String(3), nullable=False)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    player_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    player = db.relationship("User", backref="player_throws")
    round = db.relationship("Round", backref="round_throws")
