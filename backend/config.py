import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL")

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "smartwatch_ai_pro")
    DB_SSL_CA_PATH = os.environ.get("DB_SSL_CA_PATH")
    DB_SSL_ENABLED = os.environ.get("DB_SSL_ENABLED", "false").lower() == "true"

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        )

    SQLALCHEMY_ENGINE_OPTIONS = {}
    if DB_SSL_CA_PATH:
        SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {"ssl": {"ca": DB_SSL_CA_PATH}}
    elif DB_SSL_ENABLED:
        SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {"ssl": {}}

    SQLALCHEMY_TRACK_MODIFICATIONS = False
