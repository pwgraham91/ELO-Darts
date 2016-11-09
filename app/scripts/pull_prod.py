import json
import requests
import sqlalchemy as sqla
from sqlalchemy import orm

import config
from app.models import User, Game


def pull_user_data(session):
    print 'pulling users'
    user_data = requests.get(u"{}{}".format(config.base_url, 'export/users'))
    loaded_data = json.loads(user_data.text)
    for user_dict in loaded_data:
        user = User(
            id=user_dict['id'],
            name=user_dict['name'],
            email=user_dict['email'],
            admin=user_dict['admin'],
            avatar=user_dict['avatar'],
            active=user_dict['active'],
            created_at=user_dict['created_at'],
            elo=user_dict['elo'],
            wins=user_dict['wins'],
            losses=user_dict['losses']
        )
        session.add(user)
    session.commit()
    print 'done pulling users'


def pull_game_data(session):
    print 'pulling games'
    game_data = requests.get(u"{}{}".format(config.base_url, 'export/games'))
    loaded_data = json.loads(game_data.text)
    for game_dict in loaded_data:
        game = Game(
            id=game_dict['id'],
            created_at=game_dict['created_at'],
            deleted_at=game_dict['deleted_at'],
            winner_id=game_dict['winner_id'],
            winner_elo_score=game_dict['winner_elo_score'],
            loser_elo_score=game_dict['loser_elo_score'],
            submitted_by_id=game_dict['submitted_by_id']
        )
        session.add(game)
    session.commit()
    print 'done pulling games'


if __name__ == '__main__':
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    pull_user_data(session)
    pull_game_data(session)
    print 'all done'
