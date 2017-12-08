import datetime
import flask
import trueskill

from app.libs.game_lib import calc_user_current_average, get_user_most_recent_game, calc_rounds_to_win_game, get_round_dict
from app.models import Game, Round


def handle_add_game_calculations(session, game, winner, loser):
    game.winner = winner
    game.loser = loser

    winner_rating, loser_rating = trueskill.rate_1vs1(trueskill.Rating(winner.elo), trueskill.Rating(loser.elo))
    winner_elo, loser_elo = winner_rating.mu, loser_rating.mu

    game.winner_elo_score = winner_elo
    game.loser_elo_score = loser_elo

    winner.elo = winner_elo
    loser.elo = loser_elo

    winner_average = calc_user_current_average(session, winner.id, get_user_most_recent_game(session, winner.id),
                                               add_score=[winner_elo])
    winner.average_elo = winner_average
    loser_average = calc_user_current_average(session, loser.id, get_user_most_recent_game(session, loser.id),
                                              add_score=[loser_elo])
    loser.average_elo = loser_average

    winner.wins += 1
    loser.losses += 1

    game.created_at = datetime.datetime.utcnow()
    game.winner_average_score = winner_average
    game.loser_average_score = loser_average

    return winner_elo, loser_elo, winner_average, loser_average


def add_game(session, winner, loser, submitted_by_id=None, slack_user_submitted_by=None):
    if winner.id == loser.id:
        raise Exception("can't play yourself")
    if not submitted_by_id and not slack_user_submitted_by:
        raise Exception("who submitted this game?")

    new_game = Game(
        submitted_by_id=submitted_by_id,
        slack_user_submitted_by=slack_user_submitted_by
    )

    handle_add_game_calculations(session, new_game, winner, loser)

    session.add(new_game)

    return new_game


def handle_round_winner(session, round_id, round_winner_id):
    _round = session.query(Round).get(round_id)
    _round.round_winner_id = round_winner_id

    game = _round.game

    player_1_round_wins = 0
    player_2_round_wins = 0

    for game_round in game.game_rounds:
        if game_round.round_winner_id == game.in_progress_player_1_id:
            player_1_round_wins += 1
        elif game_round.round_winner_id == game.in_progress_player_2_id:
            player_2_round_wins += 1

    rounds_to_win_game = calc_rounds_to_win_game(game.best_of)

    if player_1_round_wins == rounds_to_win_game:
        handle_game_winner(session, game, game.in_progress_player_1, game.in_progress_player_2)
    elif player_2_round_wins == rounds_to_win_game:
        handle_game_winner(session, game, game.in_progress_player_2, game.in_progress_player_1)


def handle_game_winner(session, game, winner, loser):
    game.submitted_by_id = flask.g.user.id

    handle_add_game_calculations(session, game, winner, loser)


def calc_current_thrower(session, _round):
    round_dict = get_round_dict(session, _round)

    # todo finish this function
    return
