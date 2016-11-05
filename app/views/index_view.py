import flask
from app import app, db
from app.models import User


@app.route('/')
@app.route('/index')
def index():

    session = db.session

    current_user = flask.g.user

    active_users = session.query(User).all()

    return flask.render_template('index.html',
                                 title='Home',
                                 current_user=current_user,
                                 active_users=active_users)
