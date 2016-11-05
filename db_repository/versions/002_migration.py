from sqlalchemy import *
from migrate import *
import datetime


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('created_at', TIMESTAMP, nullable=False),
    Column('deleted_at', TIMESTAMP),
    Column('winner_id', BIGINT, nullable=False),
    Column('loser_id', BIGINT, nullable=False),
    Column('submitted_by', BIGINT),
)

game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_at', DateTime, nullable=False, default=ColumnDefault(datetime.datetime.now())),
    Column('deleted_at', DateTime),
    Column('winner_id', BigInteger, nullable=False),
    Column('loser_id', BigInteger, nullable=False),
    Column('submitted_by_id', BigInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['submitted_by'].drop()
    post_meta.tables['game'].columns['submitted_by_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['submitted_by'].create()
    post_meta.tables['game'].columns['submitted_by_id'].drop()
