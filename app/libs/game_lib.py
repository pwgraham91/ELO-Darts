import datetime
import sqlalchemy as sqla
from sqlalchemy import orm

import config
from app.models import User, Game


def decay_users():
    """ reduce non-playing users elo scores by 10% every 2 weeks
        redistribute elo scores to users who play
    """
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    print 'starting user decay'

    tax_rate = 10.0
    elo_tax_fund = 0

    playing_users = session.query(User).join(
        Game,
        sqla.or_(
            User.id == Game.winner_id,
            User.id == Game.loser_id
        )
    ).filter(
        Game.deleted_at.is_(False),
        Game.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=14)
    )

    non_playing_users = session.query(User).filter(
        User.id.notin_([user_.id for user_ in playing_users])
    )

    for user in non_playing_users:
        current_user_elo = user.elo
        taxed_elo = current_user_elo * (1 / tax_rate)
        user.elo = current_user_elo - taxed_elo
        session.add(user)

        elo_tax_fund += taxed_elo

    num_playing_users = playing_users.count()
    elo_distribution = elo_tax_fund /num_playing_users

    for user in playing_users:
        current_user_elo = user.elo
        user.elo = current_user_elo + elo_distribution
        session.add(user)

    session.commit()

    print 'ending user decay'

