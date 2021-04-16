import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Enum, Float


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsdkfd32r234fsdf'
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask:flask@localhost/flask_base'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


meta = MetaData()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
dataset = Table(
    'dataset', meta,
    Column('id', Integer, primary_key=True),
    Column('date', Date),
    Column('channel', String(50), nullable=False),
    Column('country', String(2), nullable=False),
    Column('os', Enum('ios', 'android', name='os')),
    Column('impressions', Integer, nullable=False),
    Column('clicks', Integer, nullable=False),
    Column('installs', Integer, nullable=False),
    Column('spend', Float, nullable=False),
    Column('revenue', Float, nullable=False)
)