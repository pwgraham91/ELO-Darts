from sqlalchemy import or_

from app.libs.datetime_lib import convert_to_local_from_utc
from app.models import User, Game


def get_profile_data(session, user_id):
    user = session.query(User).get(user_id)

    games = session.query(
        Game
    ).filter(
        or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id
        ),
        Game.deleted_at.is_(None)
    ).order_by(
        Game.created_at.desc()
    ).all()

    outcomes = []

    for game in games:
        if game.winner_id == user_id:
            opponent_name = game.loser.name
            opponent_id = game.loser_id
            outcome = 'W'
            resulting_user_elo_score = game.winner_elo_score
            resulting_opponent_elo_score = game.loser_elo_score
        else:
            opponent_name = game.winner.name
            opponent_id = game.winner_id
            outcome = 'L'
            resulting_user_elo_score = game.loser_elo_score
            resulting_opponent_elo_score = game.winner_elo_score

        game_date = convert_to_local_from_utc(game.created_at).strftime('%m/%d/%Y %I:%M %p')

        outcomes.append({
            'opponent_name': opponent_name,
            'opponent_id': opponent_id,
            'outcome': outcome,
            'date': game_date,
            'reulting_user_elo_score': resulting_user_elo_score,
            'resulting_opponent_elo_score': resulting_opponent_elo_score,
        })

    return user, outcomes
