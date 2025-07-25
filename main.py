import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from models import User, get_db
from db_init import get_admin_class, get_admin_id
from passlib.hash import bcrypt
from datetime import datetime
import socket

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def is_admin(user):
    return user and user.class_field and user.class_field[-1] >= "5"

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "msg": ""})

@app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter((User.user==username)|(User.email==username)).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Usuário ou senha inválidos"})
    if not user.is_active:
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Acesso pendente de liberação pelo admin"})
    request.session["user_id"] = user.id
    request.session["is_admin"] = is_admin(user)
    if is_admin(user):
        return RedirectResponse("/admin", status_code=302)
    else:
        return RedirectResponse("/user", status_code=302)

@app.get("/user", response_class=HTMLResponse)
def user_panel(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter_by(id=user_id).first()
    return templates.TemplateResponse("user_panel.html", {"request": request, "user": user})

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter_by(id=user_id).first()
    if not is_admin(user):
        return RedirectResponse("/login", status_code=302)
    # Lista usuários pendentes
    pending_users = db.query(User).filter_by(is_active=False).all()
    return templates.TemplateResponse("admin_panel.html", {"request": request, "user": user, "pending": pending_users})

@app.post("/admin/approve/{user_id}")
def approve_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    admin_id = request.session.get("user_id")
    admin = db.query(User).filter_by(id=admin_id).first()
    if not is_admin(admin):
        raise HTTPException(status_code=403)
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        user.is_active = True
        db.commit()
    return RedirectResponse("/admin", status_code=302)
