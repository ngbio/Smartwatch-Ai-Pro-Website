import pymysql

try:
    from backend import create_app
    from backend.config import Config
    from backend.models import db
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from backend import create_app
    from backend.config import Config
    from backend.models import db


def create_database():
    ssl_config = None
    if Config.DB_SSL_CA_PATH:
        ssl_config = {"ca": Config.DB_SSL_CA_PATH}
    elif Config.DB_SSL_ENABLED:
        ssl_config = {}

    connection = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        charset="utf8mb4",
        ssl=ssl_config,
    )

    database_name = Config.DB_NAME.replace("`", "``")

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()


def init_db():
    if not Config.DATABASE_URL:
        create_database()

    app = create_app()
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    init_db()
    print(f"Database '{Config.DB_NAME}' initialized successfully.")
