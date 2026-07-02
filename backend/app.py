from backend import app
from backend.routes.chatbot_routes import chatbot_bp
from backend.routes.product_routes import product_bp
from backend.routes.subscriber_routes import subscriber_bp


def register_api():
    app.register_blueprint(product_bp)
    app.register_blueprint(subscriber_bp)
    app.register_blueprint(chatbot_bp)


if __name__ == "__main__":
    register_api()
    app.run(debug=True)
