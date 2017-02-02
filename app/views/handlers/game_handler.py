import datetime
import trueskill

from app.libs.game_lib import calc_user_current_average, get_user_most_recent_game
from app.models import Game


def add_game(session, winner, loser, submitted_by_id=None, slack_user_submitted_by=None):
    if winner.id == loser.id:
        raise Exception("can't play yourself")
    if not submitted_by_id and not slack_user_submitted_by:
        raise Exception("who submitted this game?")

    winner_rating, loser_rating = trueskill.rate_1vs1(trueskill.Rating(winner.elo), trueskill.Rating(loser.elo))
    winner_elo, loser_elo = winner_rating.mu, loser_rating.mu

    winner_average = calc_user_current_average(session, winner.id, get_user_most_recent_game(session, winner.id),
                                               add_score=[winner_elo])
    winner.average_elo = winner_average
    loser_average = calc_user_current_average(session, loser.id, get_user_most_recent_game(session, loser.id),
                                              add_score=[loser_elo])
    loser.average_elo = loser_average

    new_game = Game(
        winner=winner,
        loser=loser,
        winner_elo_score=winner_elo,
        loser_elo_score=loser_elo,
        created_at=datetime.datetime.utcnow(),
        submitted_by_id=submitted_by_id,
        slack_user_submitted_by=slack_user_submitted_by,
        winner_average_score=winner_average,
        loser_average_score=loser_average
    )

    winner.elo = winner_elo
    loser.elo = loser_elo

    winner.wins += 1
    loser.losses += 1

    session.add_all([new_game, winner, loser])

    return new_game
