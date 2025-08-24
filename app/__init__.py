from flask import Flask
from .extensions import allow_all_cors
from .routes.chat import chat_bp
from .routes.message import message_bp
from app.extensions import init_mongo
from .routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    # Init Mongo
    init_mongo(app)
    # Init extensions
    app.url_map.strict_slashes = False
    allow_all_cors(app)

    # Load default config
    app.config.from_object("app.config.Config")

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(message_bp, url_prefix="/message")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
