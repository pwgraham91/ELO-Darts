from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('deleted_at', DateTime),
    Column('slack_user_submitted_by', String(length=64)),
    Column('score_to_0', SmallInteger, nullable=False, default=ColumnDefault(201)),
    Column('double_out', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('rebuttal', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('best_of', Integer, default=ColumnDefault(3)),
    Column('winner_id', BigInteger),
    Column('winner_elo_score', Float, nullable=False),
    Column('winner_average_score', Float),
    Column('loser_id', BigInteger),
    Column('loser_elo_score', Float),
    Column('loser_average_score', Float),
    Column('submitted_by_id', BigInteger),
    Column('in_progress_player_1_id', BigInteger),
    Column('in_progress_player_2_id', BigInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['best_of'].create()
    post_meta.tables['game'].columns['double_out'].create()
    post_meta.tables['game'].columns['in_progress_player_1_id'].create()
    post_meta.tables['game'].columns['in_progress_player_2_id'].create()
    post_meta.tables['game'].columns['rebuttal'].create()
    post_meta.tables['game'].columns['score_to_0'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['best_of'].drop()
    post_meta.tables['game'].columns['double_out'].drop()
    post_meta.tables['game'].columns['in_progress_player_1_id'].drop()
    post_meta.tables['game'].columns['in_progress_player_2_id'].drop()
    post_meta.tables['game'].columns['rebuttal'].drop()
    post_meta.tables['game'].columns['score_to_0'].drop()
