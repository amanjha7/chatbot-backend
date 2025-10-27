import json
import requests
from app.utils.common_utils import clean_and_alternate_messages

def send_chat_request(provider, model, api_key, messages):
    url = None
    headers = None

    if provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    elif provider == "perplexity":
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    elif provider == "ollama":
        url = "http://127.0.0.1:11434/api/generate"
    else:
        return None, "Unsupported provider"

    try:
        if provider == "ollama":
            prompt = messages[-1].get("content")

            response = requests.post(url, json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })

            data = response.json()
            ai_output = data.get("response") or ""
            
            formatted_resp = {
                "choices": [
                    {
                        "message": {
                            "content": ai_output
                        }
                    }
                ]
            }

            return formatted_resp, None

        body = {"model": model, "messages": clean_and_alternate_messages(messages)}
        resp = requests.post(url, headers=headers, json=body)
        return resp.json(), None

    except Exception as e:
        return None, str(e)
