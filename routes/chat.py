from flask import Blueprint, request, jsonify, current_app
from services.chat_service import send_chat_request

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.json
    provider = data.get("provider")
    model = data.get("model")
    api_key = data.get("apiKey") or current_app.config["API_KEY"]
    messages = data.get("messages")

    if not all([provider, model, api_key, messages]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        resp_json, error = send_chat_request(provider, model, api_key, messages)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(resp_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
