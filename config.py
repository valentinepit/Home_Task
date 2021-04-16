import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsdkfd32r234fsdf'
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask:flask@localhost/flask_base'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
