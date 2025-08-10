import requests
from app.utils.common_utils import clean_and_alternate_messages

def send_chat_request(provider, model, api_key, messages):
    if provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
    elif provider == "perplexity":
        url = "https://api.perplexity.ai/chat/completions"
    else:
        return None, "Unsupported provider"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {"model": model, "messages": clean_and_alternate_messages(messages)}

    resp = requests.post(url, headers=headers, json=body)
    return resp.json(), None
