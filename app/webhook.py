from fastapi import APIRouter, Request, Response
from datetime import datetime, timezone
from sqlalchemy import select
from .db import SessionLocal
from .models import FbUser, Message, Event
from .meta import send_text
from .ai import ask_ai
from .config import VERIFY_TOKEN
from services.antispam import is_spam
from services.settings import get_setting

router = APIRouter()

def now_utc():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def save_in_message(db, mid, psid, text, created_time, raw):
    db.merge(Message(
        id=mid,
        psid=psid,
        direction="in",
        text=text,
        created_time=created_time,
        raw_json=raw
    ))

def save_out_message(db, mid, psid, text, raw=None):
    db.merge(Message(
        id=mid,
        psid=psid,
        direction="out",
        text=text,
        created_time=now_utc(),
        raw_json=raw
    ))

def ensure_user(db, psid: str):
    u = db.get(FbUser, psid)
    if not u:
        u = FbUser(psid=psid, first_seen_at=now_utc(), last_seen_at=now_utc(), is_active=1)
        db.add(u)
        db.flush()
        return u, True
    u.last_seen_at = now_utc()
    u.is_active = 1
    return u, False

def handle_command(db, psid: str, text: str):
    t = (text or "").strip()
    low = t.lower()


    if low.startswith("/antispam"):
    if not is_admin(psid):
        return
    v = "on" if "on" in low else "off"
    db.execute(
        "INSERT INTO bot_settings (key,value) VALUES ('antispam',:v) "
        "ON CONFLICT (key) DO UPDATE SET value=:v",
        {"v": v}
    )
    send_text(psid, f"✅ AntiSpam = {v}")
    return

    if low == "/help":
        send_text(psid, "📌 Lệnh:\n/help\n/ai <câu hỏi>\n/stop (tắt bot)\n/start (mở lại)")
        return

    if low.startswith("/ai"):
        q = t[3:].strip()
        if not q:
            send_text(psid, "Nhập câu hỏi sau /ai nha.")
        else:
            ans = ask_ai(q)
            send_text(psid, ans)
        return

    if low == "/stop":
        u = db.get(FbUser, psid)
        if u:
            u.is_active = 0
        send_text(psid, "✅ Ok, mình sẽ không auto trả lời nữa. Gõ /start để bật lại.")
        return

    if low == "/start":
        u = db.get(FbUser, psid)
        if u:
            u.is_active = 1
        send_text(psid, "✅ Bật lại rồi nè. Gõ /help để xem lệnh.")
        return

    # Không lệnh => im lặng (theo yêu cầu vk)
    return


@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")

    return Response(content="Verification failed", status_code=403)

@router.post("/webhook")
async def receive(req: Request):
    body = await req.json()

    if body.get("object") != "page":
        return {"ok": True}

    with SessionLocal() as db:
        for entry in body.get("entry", []):
            for ev in entry.get("messaging", []):
                sender = ev.get("sender", {}).get("id")
                if not sender:
                    continue

                if get_setting(db, "antispam") == "on":
                    if is_spam(sender):
                        db.add(Event(
                            psid=sender,
                            type="spam", detail="rate limit",
                            created_at=now_utc()
                         ))
                         continue

                u, is_first = ensure_user(db, sender)

                # Postback: Get Started / menu buttons
                if "postback" in ev:
                    payload = (ev["postback"].get("payload") or "").strip()
                    db.add(Event(psid=sender, type="postback", detail=payload, created_at=now_utc()))
                    if payload == "GET_STARTED":
                        send_text(sender, "👋 Chào bạn nha! Gõ /help để xem lệnh.")
                    else:
                        # tuỳ vk map payload -> lệnh
                        send_text(sender, f"✅ Nhận nút: {payload}")
                    continue

                # Message text
                msg = ev.get("message") or {}
                mid = msg.get("mid")
                text = msg.get("text")

                if mid:
                    # created_time từ webhook là timestamp ms
                    ts = ev.get("timestamp")
                    ct = datetime.utcfromtimestamp(ts/1000.0) if ts else now_utc()
                    save_in_message(db, mid, sender, text, ct, ev)

                # Auto chào khi lần đầu nhắn (first seen)
                if is_first:
                    send_text(sender, "👋 Chào bạn nha! Gõ /help để xem lệnh.")

                # Chờ lệnh mới trả lời
                if u.is_active == 1:
                    handle_command(db, sender, text)

        db.commit()

    # quan trọng: luôn 200 OK, Meta sẽ resend nếu không 200 :contentReference[oaicite:3]{index=3}
    return {"ok": True}
