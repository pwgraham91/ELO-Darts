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
        )
    ).order_by(
        Game.created_at.desc()
    ).all()

    outcomes = []

    for game in games:

        if game.winner_id == user_id:
            outcomes.append({
                'opponent_name': '',
                'opponent_id': game.loser_id,
                'outcome': 'W',
                'date': game.created_at
            })
        else:
            outcomes.append({
                'opponent_name': '',
                'opponent_id': game.winner_id,
                'outcome': 'L',
                'date': game.created_at
            })

    return user, outcomes

