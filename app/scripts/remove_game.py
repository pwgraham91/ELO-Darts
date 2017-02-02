import datetime
import sqlalchemy as sqla
from sqlalchemy import orm
import trueskill

import config
from app.models import Game


def get_previous_game(session, user, game):
    """ given a user and a game, get previous game for user """
    previous_game = session.query(Game).filter(
        Game.deleted_at.is_(None),
        sqla.or_(
            Game.winner_id == user.id,
            Game.loser_id == user.id
        ),
        Game.id < game.id
    ).order_by(Game.id.desc()).first()

    return previous_game


def get_score_from_game(user, game):
    return game.winner_elo_score if user.id == game.winner_id else game.loser_elo_score


def get_next_game(session, user_id, last_game_id, updated_games_ids):
    return session.query(Game).filter(
        sqla.or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id
        ),
        Game.id > last_game_id,
        Game.id.notin_(updated_games_ids),
        Game.deleted_at.is_(None)
    ).first()


def replay_game(session, next_game, affected_player_ids):
    winner = next_game.winner
    loser = next_game.loser
    if next_game.winner_id in affected_player_ids:
        winner_pre_elo = winner.elo
    else:
        winner_previous_game = get_previous_game(session, winner, next_game)
        if winner_previous_game:
            winner_pre_elo = get_score_from_game(winner, winner_previous_game)
        else:
            winner_pre_elo = 100
    if next_game.loser_id in affected_player_ids:
        loser_pre_elo = loser.elo
    else:
        loser_previous_game = get_previous_game(session, loser, next_game)
        if loser_previous_game:
            loser_pre_elo = get_score_from_game(loser, loser_previous_game)
        else:
            loser_pre_elo = 100

    winner_rating, loser_rating = trueskill.rate_1vs1(trueskill.Rating(winner_pre_elo), trueskill.Rating(loser_pre_elo))
    winner_elo, loser_elo = winner_rating.mu, loser_rating.mu

    next_game.winner_elo_score = winner_elo
    next_game.loser_elo_score = loser_elo

    winner.elo = winner_elo
    loser.elo = loser_elo

    session.add_all([next_game, winner, loser])

    affected_player_ids.add(winner.id)
    affected_player_ids.add(loser.id)

    return winner, loser


def run_next_game(next_game_ids, affected_player_ids, updated_games_ids):
    if len(next_game_ids):
        next_game_id = min(next_game_ids)
        next_game = session.query(Game).get(next_game_id)
        w, l = replay_game(session, next_game, affected_player_ids)
        updated_games_ids.add(next_game_id)
        next_game_ids.remove(next_game_id)

        next_winner_game = get_next_game(session, w.id, next_game.id, updated_games_ids)
        if next_winner_game:
            next_game_ids.add(next_winner_game.id)
        next_loser_game = get_next_game(session, l.id, next_game.id, updated_games_ids)
        if next_loser_game:
            next_game_ids.add(next_loser_game.id)

        run_next_game(next_game_ids, affected_player_ids, updated_games_ids)


def remove_game(session, game_id):
    affected_player_ids = set()
    updated_games_ids = set()
    next_game_ids = set()

    game = session.query(Game).get(game_id)
    game.deleted_at = datetime.datetime.utcnow()
    session.add(game)

    winner = game.winner
    winner_previous_game = get_previous_game(session, winner, game)
    winner.elo = get_score_from_game(winner, winner_previous_game) if winner_previous_game else 100
    winner.wins -= 1
    session.add(winner)
    affected_player_ids.add(winner.id)

    loser = game.loser
    loser_previous_game = get_previous_game(session, loser, game)
    loser.elo = get_score_from_game(loser, loser_previous_game) if loser_previous_game else 100
    loser.losses -= 1
    session.add(loser)
    affected_player_ids.add(loser.id)

    next_winner_game = get_next_game(session, winner.id, winner_previous_game.id, updated_games_ids)
    if next_winner_game:
        next_game_ids.add(next_winner_game.id)

    next_loser_game = get_next_game(session, loser.id, loser_previous_game.id, updated_games_ids)
    if next_loser_game:
        next_game_ids.add(next_loser_game.id)

    run_next_game(next_game_ids, affected_player_ids, updated_games_ids)


if __name__ == '__main__':
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    # change me
    game_id = None

    remove_game(session, game_id)
    session.commit()
