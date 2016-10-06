import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
    FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    FITBIT_CLIENT_ID = 'fake_id'
    FITBIT_CLIENT_SECRET = 'fake_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


def get_current_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'prod': ProductionConfig
}
