import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '1234567891@123'
    # SQLALCHEMY_DATABASE_URI = 'postgres://vuonglv:vuonglv@db.pythonistavn.com:5432/techblog'
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:dinhngoc2000@@localhost:5432/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
