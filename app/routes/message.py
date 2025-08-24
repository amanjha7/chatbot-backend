from flask import Blueprint, request, jsonify, current_app
from app.models.messages import MessageModel
from app.middleware import require_api_key

message_bp = Blueprint("message", __name__)

@message_bp.route("/add", methods=["POST"])
@require_api_key
def add_message():
    data = request.json
    message_id = MessageModel.create(
        message=data.get("message"),
        role=data.get("role", "user"),
        chatId=data.get("chat_id")
    )
    return jsonify({"status": "success", "id": str(message_id)})

@message_bp.route("/", methods=["GET"])
@require_api_key
def get_messages():
    return jsonify(MessageModel.get_all())

@message_bp.route("/<chatID>", methods=["GET"])
@require_api_key
def get_messages_chat_id(chatID):
    return jsonify(MessageModel.get_messages_by_chat_id(chatID))