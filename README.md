# ELO-Darts

## Set Up

### Install requirements

#### Install python requirements
`pip install -r requirements`

#### Install javascript requirements
`bower install`

### Setup database
Make sure your local database is running and open it with
`psql postgres`

Create a new database with `CREATE DATABASE elo_darts`

`python db_create.py`

`python db_migrate.py`

### Create config
In the root directory, make a file called config.py using example_config.py as a template then replace all of the keys with your own

## Run the app
`python run.py`
