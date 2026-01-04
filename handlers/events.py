from datetime import datetime
from db import get_conn

def on_member_added(psid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO fb_users(psid, first_seen_at)
            VALUES (%s, %s)
            ON CONFLICT (psid) DO NOTHING
        """, (psid, datetime.utcnow()))
    return "👋 Chào thành viên mới đã gia nhập nhóm nha!"

def on_member_removed(psid):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE fb_users SET is_active=0 WHERE psid=%s", (psid,))
    return "👋 Vĩnh biệt, không hẹn gặp lại.Tiễn vong!"
