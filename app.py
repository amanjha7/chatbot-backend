from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = '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'

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    provider = data.get("provider")
    model = data.get("model")
    api_key = data.get("apiKey") or API_KEY
    messages = data.get("messages")

    if not all([provider, model, api_key, messages]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        if provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            body = {"model": model, "messages": messages}

        elif provider == "perplexity":
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            body = {"model": model, "messages": messages}

        else:
            return jsonify({"error": "Unsupported provider"}), 400

        resp = requests.post(url, headers=headers, json=body)
        return jsonify(resp.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
