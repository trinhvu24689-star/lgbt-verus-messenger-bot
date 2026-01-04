import os
from dotenv import load_dotenv

load_dotenv()

APP_SECRET = os.getenv("APP_SECRET", "change_me")
ADMIN_KEY = os.getenv("ADMIN_KEY", "QTV123")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "")
PAGE_ID = os.getenv("PAGE_ID", "")

DATABASE_URL = os.getenv("DATABASE_URL")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL chưa được set trong env")
if not PAGE_ACCESS_TOKEN:
    print("⚠️ PAGE_ACCESS_TOKEN chưa set")