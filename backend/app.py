from pathlib import Path
import sys

try:
    from backend import app
    from backend.routes import api
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from backend import app
    from backend.routes import api


def register_api():
    app.register_blueprint(api, url_prefix="/api")


if __name__ == "__main__":
    register_api()
    app.run(debug=True)
