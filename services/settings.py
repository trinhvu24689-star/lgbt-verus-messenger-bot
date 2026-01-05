from sqlalchemy import select
from app.models import Event
from app.db import SessionLocal

def get_setting(db, key: str, default="off"):
    r = db.execute(
        "SELECT value FROM bot_settings WHERE key=:k",
        {"k": key}
    ).fetchone()
    return r[0] if r else default
