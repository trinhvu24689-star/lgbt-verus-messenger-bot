from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from .webhook import router as webhook_router
from .admin import router as admin_router
from .db import Base, engine
from .sync_old import sync_conversations

app = FastAPI(title="Messenger Bot + CRM")

Base.metadata.create_all(bind=engine)

app.include_router(webhook_router)
app.include_router(admin_router)

sched = BackgroundScheduler()

@sched.scheduled_job("interval", minutes=10)
def job_sync():
    # quét hội thoại cũ (sườn)
    sync_conversations(limit=25)

sched.start()