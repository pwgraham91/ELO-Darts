import flask
from app import app, db
from app.views.handlers.auth_handler import get_google_authorization_url
from app.views.handlers.user_handler import get_active_users


@app.route('/test_bugsnag')
def test_bugsnag():

    session = db.session

    current_user = flask.g.user
    a = 1
    a += 'this shouldnt work'

    active_users = get_active_users(session)

    return flask.render_template('index.html',
                                 title='Cratejoy Darts',
                                 current_user=current_user,
                                 active_users=active_users,
                                 auth_url=get_google_authorization_url())
