import flask
import sqlalchemy as sqla

from app import app, db
from app.models import Game
from app.views.handlers.auth_handler import get_google_authorization_url
from app.views.handlers.profile_handler import get_profile_data
from app.views.handlers.user_handler import get_active_users


@app.route('/profile/<int:user_id>')
def get_profile(user_id):

    session = db.session

    user, results = get_profile_data(session, user_id)

    user_games = session.query(Game).filter(
        sqla.or_(
            Game.winner_id == user_id,
            Game.loser_id == user_id,
        ),
        Game.deleted_at.is_(None)
    ).order_by(Game.created_at).all()

    return flask.render_template('user.html',
                                 title=user.name,
                                 user=user,
                                 results=results,
                                 auth_url=get_google_authorization_url(),
                                 user_games=[game.dict for game in user_games],
                                 active_users=get_active_users(session)  # used in base for 'Add Game'
                                 )
