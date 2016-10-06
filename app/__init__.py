from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

db = SQLAlchemy()
csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    db.app = app

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
