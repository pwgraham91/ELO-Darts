from sqlalchemy import or_
from app.models import User, Game


def get_profile(session, user_id):
    user = session.query(User).get(user_id)

    games = session.query(Game).filter(
        or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id
        )
    ).order_by(
        Game.created_at.desc()
    )

    return user, games

