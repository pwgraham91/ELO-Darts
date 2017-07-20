#!flask/bin/python

from app import app
import config


if config.ENVIRONMENT == 'prod':
    import bugsnag
    from bugsnag.flask import handle_exceptions

    bugsnag.configure(api_key=config.BUGSNAG_API_KEY, project_root='/app')
    handle_exceptions(app)

app.run(debug=config.debug, port=8000)
