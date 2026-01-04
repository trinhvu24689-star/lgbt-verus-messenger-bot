from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, desc
from .db import SessionLocal
from .models import FbUser, Message
from .config import ADMIN_KEY

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def authed(req: Request) -> bool:
    return req.cookies.get("admin") == ADMIN_KEY

@router.get("/admin", response_class=HTMLResponse)
def admin_home(req: Request):
    if not authed(req):
        return templates.TemplateResponse("login.html", {"request": req})
    with SessionLocal() as db:
        users = db.execute(select(FbUser).order_by(desc(FbUser.last_seen_at)).limit(50)).scalars().all()
    return templates.TemplateResponse("dashboard.html", {"request": req, "users": users})

@router.post("/admin/login")
def admin_login(key: str = Form(...)):
    if key != ADMIN_KEY:
        return RedirectResponse("/admin", status_code=302)
    resp = RedirectResponse("/admin", status_code=302)
    resp.set_cookie("admin", ADMIN_KEY, httponly=True)
    return resp

@router.get("/admin/u/{psid}", response_class=HTMLResponse)
def view_user(req: Request, psid: str):
    if not authed(req):
        return RedirectResponse("/admin", status_code=302)
    with SessionLocal() as db:
        msgs = db.execute(
            select(Message).where(Message.psid == psid).order_by(desc(Message.created_time)).limit(200)
        ).scalars().all()
    return templates.TemplateResponse("conversation.html", {"request": req, "psid": psid, "msgs": msgs})
