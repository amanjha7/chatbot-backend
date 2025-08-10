# extensions.py
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()
mongo = PyMongo()

def allow_all_cors(app):
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    return app

def init_mongo(app):
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") + "/" + os.getenv("MONGO_DB")
    mongo.init_app(app)