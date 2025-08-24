from flask import Blueprint, request, jsonify, current_app
from app.models.user import UserModel
import jwt
from datetime import datetime, timezone, timedelta
from loguru import logger

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")  # Password is not used in this example

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400
    
    if UserModel.check_user_exists(email):
        return jsonify({"error": "User with this email already exists"}), 400

    user_id = UserModel.create(username, email, password)
    user = UserModel.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User creation failed"}), 500
    logger.info(f"User created with ID: {user_id}")
    logger.info(f"User details: {user}")
    secret_key = current_app.config.get("SECRET_KEY", "default_secret")
    token = jwt.encode({'public_id': user["id"], 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, secret_key, algorithm="HS256")
    return jsonify({"status": "success", "token":token}), 201

@auth_bp.route("/login", methods=["POST"])
def validate():
    data = request.json
    password = data.get("password")
    email = data.get("email")

    if not password or not email:
        return jsonify({"error": "Username and email are required"}), 400

    user = UserModel.validate_user(password, email)
    if not user:
        return jsonify({"valid": False}), 200
    else:
        secret_key = current_app.config.get("SECRET_KEY", "default_secret")
        token = jwt.encode({'public_id': user['id'], 'exp': datetime.now(timezone.utc) + timedelta(hours=24)}, secret_key, algorithm="HS256")
        return jsonify({"valid": True, "token": token}), 200