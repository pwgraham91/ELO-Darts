import flask

from app import app


@app.route('/')
@app.route('/index')
def index():
    user = flask.g.user
    return flask.render_template('index.html',
                                 title='Home',
                                 user=user)
