import datetime
import trueskill

from app.models import Game


def add_game(session, winner, loser, submitted_by_id=None, slack_user_submitted_by=None):
    if winner.id == loser.id:
        raise Exception("can't play yourself")
    if not submitted_by_id and not slack_user_submitted_by:
        raise Exception("who submitted this game?")

    winner_rating, loser_rating = trueskill.rate_1vs1(trueskill.Rating(winner.elo), trueskill.Rating(loser.elo))
    winner_elo, loser_elo = winner_rating.mu, loser_rating.mu

    new_game = Game(
        winner=winner,
        loser=loser,
        winner_elo_score=winner_elo,
        loser_elo_score=loser_elo,
        created_at=datetime.datetime.utcnow(),
        submitted_by_id=submitted_by_id,
        slack_user_submitted_by=slack_user_submitted_by
    )

    winner.elo = winner_elo
    loser.elo = loser_elo

    winner.wins += 1
    loser.losses += 1

    session.add_all([new_game, winner, loser])

    return new_game
