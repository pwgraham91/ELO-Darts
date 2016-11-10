from datetime import datetime
from sqlalchemy import or_
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
        else:
            opponent_name = game.winner.name
            opponent_id = game.winner_id
            outcome = 'L'

        game_date = game.created_at.strftime('%m/%d/%Y %H:%M')

        outcomes.append({
            'opponent_name': opponent_name,
            'opponent_id': opponent_id,
            'outcome': outcome,
            'date': game_date
        })

    return user, outcomes

