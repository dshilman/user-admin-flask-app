import json
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, url_for
from flask.logging import default_handler
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask.cli import AppGroup


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
database = SQLAlchemy(metadata=metadata)
db_migration = Migrate()

csrf_protection = CSRFProtect()
login = LoginManager()
login.session_protection = "strong"
login.login_view = "auth.login"

seed_cli = AppGroup('seed')


def create_app():
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_error_pages(app)

    return app

@seed_cli.command('run')
def seed_command():
    """Seeds the database"""
    print("Seeding database")
    from data_load import populate_db
    populate_db()
    
@seed_cli.command('clean')
def seed_clean():
    """Cleans out the database"""
    print("Deleting all data")
    from data_load import clean_db 
    clean_db()
 

def register_blueprints(app: Flask):
    from .auth import auth_blueprint
    from .users import users_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(users_blueprint, url_prefix="/users")



def configure_logging(app: Flask):

    if app.config.get("LOG_WITH_GUNICORN") is not None:
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.INFO)
    else:
        file_handler = RotatingFileHandler(
            "instance/flask-app.log", maxBytes=16384, backupCount=20
        )
        file_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info("Starting the Flask App...")


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    database.init_app(app)
    db_migration.init_app(app, database)
    csrf_protection.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from .models import User

    @login.user_loader
    def load_user(user_id):
        user: User = User.query.get(user_id)
        # user.roles = [user.role]
        return user


def register_error_pages(app):

    @app.errorhandler(403)
    def unauthorizedd(e):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def page_not_found(e):
        return render_template("405.html"), 405

    @app.errorhandler(500)
    def unhandled_error(e):
        return render_template("500.html"), 500


from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


from functools import wraps

from flask import abort
from flask_security import current_user, login_required


def required_roles(roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role in roles:
                return f(*args, **kwargs)
            
            abort(403)

        return wrapped

    return wrapper
