# ELO-Darts

## Set Up

### Get a virtual environment
`mkvirtualenv flask_template`

Use `workon` to activate a virtual environment or `deactivate` to leave
a virtual environment. If this doesn't work, make sure you have 
virtualenvironment wrapper installed in pip

### Install requirements
`pip install -r requirements`

### Setup database
Make sure your local database is running and open it with
`psql postgres`

Create a new database with `CREATE DATABASE elo_darts`

`python db_create.py`

`python db_migrate.py`

### Run the app
`python run.py`
