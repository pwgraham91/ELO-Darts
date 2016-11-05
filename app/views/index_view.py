import flask
from app import app, db
from app.models import User
from app.views.handlers.auth_handler import get_google_authorization_url


@app.route('/')
@app.route('/index')
def index():

    session = db.session

    current_user = flask.g.user

    active_users = session.query(User).all()

    return flask.render_template('index.html',
                                 title='Home',
                                 current_user=current_user,
                                 active_users=active_users,
                                 auth_url=get_google_authorization_url())
