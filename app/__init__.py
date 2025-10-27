from flask import Flask
from .extensions import allow_all_cors
from .routes.chat import chat_bp
from .routes.message import message_bp
from app.extensions import init_mongo
from .routes.auth import auth_bp
from app.extensions import mail
from .config import Config

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

    app.config["MAIL_SERVER"]= Config.MAIL_SERVER
    app.config["MAIL_PORT"] = Config.MAIL_PORT  
    app.config["MAIL_USE_TLS"] = Config.MAIL_USE_TLS
    app.config["MAIL_USERNAME"] = Config.MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = Config.MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = Config.MAIL_DEFAULT_SENDER

    mail.init_app(app)

    return app
