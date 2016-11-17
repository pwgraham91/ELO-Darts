import flask
from app import app, db
from app.views.handlers.auth_handler import get_google_authorization_url
from app.views.handlers.profile_handler import get_profile_data
from app.views.handlers.user_handler import get_active_users


@app.route('/profile/<int:user_id>')
def get_profile(user_id):

    session = db.session

    user, results = get_profile_data(session, user_id)

    active_users = get_active_users(session)

    return flask.render_template('user.html',
                                 title=user.name,
                                 user=user,
                                 active_users=active_users,
                                 results=results,
                                 auth_url=get_google_authorization_url())
