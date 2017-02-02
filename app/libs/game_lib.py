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


def calc_user_current_average(session, user_id, game_id, add_score=None):
    user_current_winning_game_elo_scores = session.query(sqla.func.array_agg(Game.winner_elo_score)).filter(
        Game.id <= game_id,
        Game.winner_id == user_id
    ).all()
    user_current_loser_game_elo_scores = session.query(sqla.func.array_agg(Game.loser_elo_score)).filter(
        Game.id <= game_id,
        Game.loser_id == user_id
    ).all()

    # [0][0] to access the nested array of values. if no scores, it will return None so instead set to empty list
    winner_score_values = user_current_winning_game_elo_scores[0][0] or []
    loser_score_values = user_current_loser_game_elo_scores[0][0] or []

    combined_scores = winner_score_values + loser_score_values
    if add_score:
        combined_scores += add_score
    return sum(combined_scores) / len(combined_scores)


def get_user_most_recent_game(session, user_id):
    game_id_result = session.query(Game.id).filter(
        sqla.or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id
        )
    ).order_by(Game.id.desc()).first()

    if game_id_result:
        return game_id_result[0]
