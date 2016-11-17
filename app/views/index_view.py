import flask
from app import app, db
from app.views.handlers.auth_handler import get_google_authorization_url
from app.views.handlers.user_handler import get_active_users


@app.route('/')
@app.route('/index')
def index():

    session = db.session

    current_user = flask.g.user

    active_users = get_active_users(session)

    return flask.render_template('index.html',
                                 title='Cratejoy Darts',
                                 current_user=current_user,
                                 active_users=active_users,
                                 auth_url=get_google_authorization_url())
