import logging
import os
import secrets
from datetime import timedelta


BASEDIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    WTF_CSRF_ENABLED = True
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default=secrets.token_hex())
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=14)



class ProductionConfig(Config):
    FLASK_ENV = "production"
    logt_level = logging.INFO
    LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)


class DevelopmentConfig(Config):
    log_level = logging.DEBUG
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

