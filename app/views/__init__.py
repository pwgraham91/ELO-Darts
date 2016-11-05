import flask
from flask_login import current_user

from app import app
import load_views


@app.before_request
def before_request():
    flask.g.user = current_user
