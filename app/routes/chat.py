from flask import Blueprint, request, jsonify, current_app
from app.services.chat_service import send_chat_request
from app.models.messages import MessageModel
from app.models.chats import ChatModel
from datetime import datetime, timezone

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.json
    provider = data.get("provider")
    model = data.get("model")
    api_key = data.get("apiKey") or current_app.config["API_KEY"]
    messages = data.get("messages")
    chat_id = data.get("chat_id")

    if not all([provider, model, api_key, messages]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        resp_json, error = send_chat_request(provider, model, api_key, messages)
        if error:
            return jsonify({"error": error}), 400
        update_message_to_db(messages, chat_id, resp_json)
        return jsonify(resp_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_message_to_db(messages, chat_id, resp_json):
    ai_response = (
            resp_json.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content")
            or resp_json.get("output")
            or "No Response from AI"
        )
    message_obj = {
            "role" : "assistant",
            "content" : ai_response,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
        }
    messages.append(message_obj)
    update_message(chatId=chat_id,message=messages)
    

@chat_bp.route("/add",methods=["POST"])
def add_chat():
    data = request.json
    ChatModel.create(
        title=data.get("title") or "Title",
        chatId=data.get("chat_id")
    )
    return jsonify({"status":"Successfilly created Chat"}), 200

@chat_bp.route("/",methods=["GET"])
def get_all_chats():
    chats = ChatModel.get_all()
    return jsonify(chats)

def add_message(chatId, message, role, created_at):
    message = MessageModel.create(
        message=message,role=role,chat_id=chatId
    )
    
def update_message(chatId,message):
    print("Updating Message")
    MessageModel.update_by_chat_id(
        chatId=chatId,message=message
    )