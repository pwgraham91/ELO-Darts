import trueskill

from app.models import User, Game


def add_game(session, winner_id, loser_id, submitted_by_id):
    if winner_id == loser_id:
        raise Exception("can't play yourself")

    winner = session.query(User).get(winner_id)
    loser = session.query(User).get(loser_id)
    submitted_by = session.query(User).get(submitted_by_id)

    winner_rating, loser_rating = trueskill.rate_1vs1(trueskill.Rating(winner.elo), trueskill.Rating(loser.elo))
    winner_elo, loser_elo = winner_rating.mu, loser_rating.mu

    # verify created at

    new_game = Game(
        winner=winner,
        loser=loser,
        submitted_by=submitted_by,
        winner_elo_score=winner_elo,
        loser_elo_score=loser_elo,
    )

    winner.elo = winner_elo
    loser.elo = loser_elo

    session.add_all([new_game, winner, loser])

    return new_game

