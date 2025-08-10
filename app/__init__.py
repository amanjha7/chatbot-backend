from flask import Flask
from .extensions import allow_all_cors
from routes.chat import chat_bp

def create_app():
    app = Flask(__name__)
    # Init extensions
    app.url_map.strict_slashes = False
    allow_all_cors(app)

    # Load default config
    app.config.from_object("app.config.Config")

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix="/chat")

    return app
