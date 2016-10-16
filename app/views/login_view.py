import flask
from flask_login import logout_user

from app import app, oid
from app.forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if flask.g.user is not None and flask.g.user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flask.session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return flask.render_template('login.html',
                                 title='Sign In',
                                 form=form,
                                 providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))
