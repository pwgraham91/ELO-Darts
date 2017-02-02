import sqlalchemy as sqla
from sqlalchemy import orm

import config
from app.libs.game_lib import calc_user_current_average
from app.models import Game


def backfill_games(session):
    for game in session.query(Game).order_by(Game.id.asc()).all():
        winner = game.winner
        winner_average = calc_user_current_average(winner.id, game.id)
        winner.average_elo = winner_average
        game.winner_average_score = winner_average

        loser = game.loser
        loser_average = calc_user_current_average(loser.id, game.id)
        loser.average_elo = loser_average
        game.loser_average_score = loser_average

        session.add_all([game, winner, loser])


if __name__ == '__main__':
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    backfill_games(session)

    session.commit()
