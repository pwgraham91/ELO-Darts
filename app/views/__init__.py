import flask
from flask_login import current_user, login_user

from app import app, oid, db, lm
from app.models import User
import load_views


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flask.flash('Invalid login. Please try again.')
        return flask.redirect(flask.url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        user = User(name=resp.nickname or resp.email.split('@')[0], email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in flask.session:
        remember_me = flask.session['remember_me']
        flask.session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return flask.redirect(flask.url_for('index'))

@app.before_request
def before_request():
    flask.g.user = current_user
