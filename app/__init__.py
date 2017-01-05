from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

# plugin decelar
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # plugin init
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # add-on route
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
