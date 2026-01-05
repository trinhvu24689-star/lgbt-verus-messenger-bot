import requests

API = "https://libretranslate.de/translate"

def translate_auto(text: str):
    payload = {
        "q": text,
        "source": "auto",
        "target": "vi",
        "format": "text"
    }
    r = requests.post(API, data=payload, timeout=10)
    if r.status_code != 200:
        return None
    return r.json().get("translatedText")
