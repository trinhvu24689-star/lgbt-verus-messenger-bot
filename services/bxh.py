from sqlalchemy import text
from datetime import datetime, timedelta

def get_bxh(db, mode="ngay", limit=10):
    now = datetime.utcnow()

    if mode == "ngay":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif mode == "thang":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:  # nam
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    q = text("""
        SELECT psid, COUNT(*) AS cnt
        FROM messages
        WHERE direction='in' AND created_time >= :start
        GROUP BY psid
        ORDER BY cnt DESC
        LIMIT :limit
    """)

    return db.execute(q, {"start": start, "limit": limit}).fetchall()
