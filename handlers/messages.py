import json
from datetime import datetime
from db import get_conn

def log_message(msg_id, conv_id, psid, direction, text, raw):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO messages
            (id, conversation_id, psid, direction, text, created_time, raw_json)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING
        """, (
            msg_id, conv_id, psid, direction,
            text, datetime.utcnow(), json.dumps(raw)
        ))