from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.config import Config


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    CORS(app)

    from app.routes.user import account
    from app.routes.todo import todo

    app.register_blueprint(account)
    app.register_blueprint(todo)

    return app
