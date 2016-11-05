import flask
from app import app, db
from app.views.handlers.profile_handler import get_profile


@app.route('/profile/<int:user_id>')
def get_profile(user_id):

    session = db.session

    user, games = get_profile(session, user_id)

    return flask.render_template('user.html',
                                 title=user.name,
                                 user=user,
                                 games=games)
