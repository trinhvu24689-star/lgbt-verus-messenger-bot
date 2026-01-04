from datetime import datetime
from sqlalchemy import select
from .db import SessionLocal
from .models import Conversation, Message
from .meta import graph_get
from .config import PAGE_ID

def parse_time(t: str):
    # Meta thường trả ISO8601 hoặc unix; best-effort
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None

def sync_conversations(limit=25):
    with SessionLocal() as db:
        code, j = graph_get(f"/{PAGE_ID}/conversations", {"limit": limit})
        if code != 200:
            return False, j

        for c in j.get("data", []):
            cid = c.get("id")
            ut = c.get("updated_time")
            db.merge(Conversation(id=cid, updated_time=parse_time(ut) if ut else None))

            # lấy message ids
            code2, j2 = graph_get(f"/{cid}", {"fields": "messages{created_time,id}"})
            msgs = (j2.get("messages") or {}).get("data") or []
            for m in msgs:
                mid = m.get("id")
                # chỉ lưu “sườn” để tránh gọi /MESSAGE-ID quá nhiều
                if mid:
                    if not db.get(Message, mid):
                        db.merge(Message(id=mid, conversation_id=cid, direction="in", created_time=parse_time(m.get("created_time"))))
        db.commit()
    return True, {"ok": True}
