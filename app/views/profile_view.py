import flask
from app import app, db
from app.views.handlers.profile_handler import get_profile_data


@app.route('/profile/<int:user_id>')
def get_profile(user_id):

    session = db.session

    user, results = get_profile_data(session, user_id)

    return flask.render_template('user.html',
                                 title=user.name,
                                 user=user,
                                 results=results)
