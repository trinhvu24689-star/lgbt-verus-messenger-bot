import requests
from .config import PAGE_ACCESS_TOKEN

GRAPH = "https://graph.facebook.com/v19.0"

def graph_get(path: str, params: dict):
    url = f"{GRAPH}/{path.lstrip('/')}"
    p = dict(params or {})
    p["access_token"] = PAGE_ACCESS_TOKEN
    r = requests.get(url, params=p, timeout=30)
    return r.status_code, r.json()

def graph_post(path: str, payload: dict):
    url = f"{GRAPH}/{path.lstrip('/')}"
    r = requests.post(url, params={"access_token": PAGE_ACCESS_TOKEN}, json=payload, timeout=30)
    return r.status_code, r.json()

def send_text(psid: str, text: str):
    payload = {
        "recipient": {"id": psid},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    return graph_post("/me/messages", payload)
