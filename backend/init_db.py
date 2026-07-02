try:
    from backend import app, db
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from backend import app, db


def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
