import requests
from .config import OPENAI_API_KEY, OPENAI_MODEL

def ask_ai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return "⚠️ Chưa cấu hình OPENAI_API_KEY nên chưa dùng AI được."

    # Call OpenAI Responses API (simple)
    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": OPENAI_MODEL,
        "input": prompt
    }
    r = requests.post(url, headers=headers, json=data, timeout=60)
    if r.status_code != 200:
        return f"⚠️ AI lỗi ({r.status_code})."
    j = r.json()
    # best-effort extract text
    try:
        return j["output"][0]["content"][0]["text"]
    except Exception:
        return "⚠️ AI trả về nhưng không đọc được format."
