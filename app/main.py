from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from passlib.hash import bcrypt
from models import SessionLocal, User, ConfigVar
import uvicorn

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='ultrasecret')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "msg": ""})

@app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        (User.user == username) | (User.email == username)
    ).first()
    if user and bcrypt.verify(password, user.password_hash):
        request.session["user_id"] = user.id
        request.session["user_class"] = user.class_field
        if user.class_field and user.class_field[-1] >= "5":
            return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
        return RedirectResponse(url="/user", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Usuário ou senha incorretos!"})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "register": True, "msg": ""})

@app.post("/register", response_class=HTMLResponse)
def register_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter((User.user == username) | (User.email == email)).first():
        return templates.TemplateResponse("login.html", {"request": request, "register": True, "msg": "Usuário ou email já cadastrado."})
    new_user = User(
        user=username,
        email=email,
        password_hash=bcrypt.hash(password),
        class_field="00000",
        is_active=False
    )
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("login.html", {"request": request, "msg": "Usuário cadastrado. Aguarde liberação do admin."})

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user_class = request.session.get("user_class", "")
    if not user_id or not (user_class and user_class[-1] >= "5"):
        return RedirectResponse(url="/login")
    users = db.query(User).all()
    config = db.query(ConfigVar).all()
    return templates.TemplateResponse("admin_panel.html", {"request": request, "users": users, "config": config})

@app.post("/admin/activate")
def admin_activate_user(request: Request, user_id: int = Form(...), db: Session = Depends(get_db)):
    admin_id = request.session.get("user_id")
    user_class = request.session.get("user_class", "")
    if not admin_id or not (user_class and user_class[-1] >= "5"):
        return RedirectResponse(url="/login")
    user = db.query(User).get(user_id)
    if user:
        user.is_active = True
        user.class_field = "00001"
        db.commit()
    return RedirectResponse(url="/admin", status_code=302)

@app.get("/user", response_class=HTMLResponse)
def user_panel(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).get(user_id) if user_id else None
    if not user or not user.is_active:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("user_panel.html", {"request": request, "user": user})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
