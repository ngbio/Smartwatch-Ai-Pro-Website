from flask import Flask
from flask_cors import CORS

from .config import Config
from .models import db
from .routes import api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    app.register_blueprint(api, url_prefix="/api")

    return app
