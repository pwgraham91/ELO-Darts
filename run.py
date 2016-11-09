#!flask/bin/python

from app import app
import config

app.run(debug=config.debug, port=8000)
