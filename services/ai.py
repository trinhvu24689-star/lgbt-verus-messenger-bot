import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def ai_reply(text):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":"Bạn là bot hỗ trợ thân thiện,đóng vai người chồng phản diện.Nghiêm khắc với hành vi đồi trụy,cụ thể là chửi luôn."},
            {"role":"user","content": text}
        ]
    )
    return r.choices[0].message.content
