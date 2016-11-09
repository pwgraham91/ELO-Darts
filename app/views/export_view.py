import json

import flask

from app import app, db
from app.models import User, Game


@app.route('/export/users', methods=['GET'])
def export_users():
    session = db.session
    return flask.Response(json.dumps([user.dict for user in session.query(User).all()]), mimetype=u'application/json')


@app.route('/export/games', methods=['GET'])
def export_games():
    session = db.session
    return flask.Response(json.dumps([game.dict for game in session.query(Game).all()]), mimetype=u'application/json')
