from sqlalchemy import *
from migrate import *
import datetime


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('admin', Boolean, default=ColumnDefault(False)),
    Column('avatar', String(length=200)),
    Column('active', Boolean, default=ColumnDefault(True)),
    Column('created_at', DateTime, nullable=False, default=ColumnDefault(datetime.datetime.utcnow())),
    Column('elo', Float, default=ColumnDefault(100.0)),
    Column('wins', Integer, nullable=False, default=ColumnDefault(0)),
    Column('losses', Integer, nullable=False, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['losses'].create()
    post_meta.tables['user'].columns['wins'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['losses'].drop()
    post_meta.tables['user'].columns['wins'].drop()
