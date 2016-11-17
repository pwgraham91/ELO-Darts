import flask

from requests_oauthlib import OAuth2Session

from config import Auth


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI,
            scope=['email']
        )
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=['email']
    )
    return oauth


def get_google_authorization_url():
    current_user = flask.g.user

    if current_user.is_authenticated:
        return

    google = get_google_auth()

    auth_url, state = google.authorization_url(Auth.AUTH_URI)

    flask.session['oauth_state'] = state
    return auth_url
