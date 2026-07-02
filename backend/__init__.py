import os
from urllib.parse import quote_plus

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

AIVEN_DB_HOST = os.environ.get("AIVEN_DB_HOST", "localhost")
AIVEN_DB_PORT = os.environ.get("AIVEN_DB_PORT", "3306")
AIVEN_DB_USER = os.environ.get("AIVEN_DB_USER", "root")
AIVEN_DB_PASSWORD = os.environ.get("AIVEN_DB_PASSWORD", "")
AIVEN_DB_NAME = os.environ.get("AIVEN_DB_NAME", "smartwatch_ai_pro")
AIVEN_DB_SSL_CA = os.environ.get("AIVEN_DB_SSL_CA")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{quote_plus(AIVEN_DB_USER)}:{quote_plus(AIVEN_DB_PASSWORD)}"
    f"@{AIVEN_DB_HOST}:{AIVEN_DB_PORT}/{AIVEN_DB_NAME}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

if AIVEN_DB_SSL_CA:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"ssl": {"ca": AIVEN_DB_SSL_CA}}
    }
else:
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"ssl": {}}}

db = SQLAlchemy(app=app)
