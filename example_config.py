import os

basedir = os.path.abspath(os.path.dirname(__file__))

# WTF
WTF_CSRF_ENABLED = True
SECRET_KEY = 'some-uuid'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/elo_darts'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class Auth:
    CLIENT_ID = 'yourclientid.apps.googleusercontent.com'
    CLIENT_SECRET = 'GduvUs0-yourclientsecred'
    # use ngrok for local
    REDIRECT_URI = 'https://cratejoydarts.pw/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'

slack_token = u'yourSlackToken'

debug = True
ENVIRONMENT = 'dev'

base_url = 'http://127.0.0.1:8000/'
prod_url = 'https://www.cratejoydarts.pw/'
