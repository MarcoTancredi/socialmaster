import os

ROOT = "socialmaster"
os.makedirs(ROOT, exist_ok=True)
os.makedirs(os.path.join(ROOT, "templates"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "static"), exist_ok=True)

files = {
    "requirements.txt": """fastapi
uvicorn[standard]
sqlalchemy
passlib[bcrypt]
python-multipart
jinja2
""",
    "main.py": '''
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
''',

    "models.py": '''
from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

DATABASE_URL = "sqlite:///socialmaster.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(64), unique=True, nullable=False)
    company = Column(String(64))
    phone = Column(String(32))
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    class_field = Column(String(5), default="00000")
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime)
    last_accessed_ip = Column(String(32))
''',

    "db_init.py": '''
from models import Base, engine, SessionLocal, User
from passlib.hash import bcrypt

def get_admin_class():
    return "99999"

def get_admin_id():
    return 1

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Cria usuário admin se não houver nenhum
    if not db.query(User).first():
        admin = User(
            user="goofy",
            company="Acme",
            phone="localhost",
            email="goofy@acme.com",
            password_hash=bcrypt.hash("8569658Zz!."),
            class_field=get_admin_class(),
            is_active=True
        )
        db.add(admin)
        db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
''',

    "templates/login.html": '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Login - SocialMaster</title>
    <link rel="stylesheet" href="/static/neon.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="bg-neon">
    <div class="container-neon">
        <h2 class="title-neon">SocialMaster - Login</h2>
        <form method="post" action="/login" class="form-neon">
            <input type="text" name="username" placeholder="Usuário ou E-mail" required>
            <input type="password" name="password" placeholder="Senha" required>
            <div class="form-row">
                <input type="checkbox" name="keep_logged" id="keep_logged">
                <label for="keep_logged">Manter-me conectado</label>
            </div>
            <button type="submit" class="btn-neon">Entrar</button>
            <div class="links-neon">
                <a href="#">Esqueci a senha</a> |
                <a href="#">Primeiro acesso? Cadastre-se.</a>
            </div>
        </form>
        {% if msg %}
        <div class="msg-neon">{{msg}}</div>
        {% endif %}
    </div>
</body>
</html>
''',

    "templates/user_panel.html": '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel do Usuário - SocialMaster</title>
    <link rel="stylesheet" href="/static/neon.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="bg-neon">
    <div class="container-neon">
        <h2 class="title-neon">Bem-vindo, {{ user.user }}</h2>
        <p>Você está autenticado como usuário comum.</p>
        <a href="/login" class="btn-neon">Sair</a>
    </div>
</body>
</html>
''',

    "templates/admin_panel.html": '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Painel Admin - SocialMaster</title>
    <link rel="stylesheet" href="/static/neon.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body class="bg-neon">
    <div class="container-neon">
        <h2 class="title-neon">Painel do Administrador</h2>
        <h3>Pedidos de cadastro pendentes:</h3>
        {% if pending %}
        <ul>
            {% for u in pending %}
            <li>
                {{ u.user }} ({{ u.email }}) 
                <form method="post" action="/admin/approve/{{u.id}}" style="display:inline">
                    <button class="btn-neon" type="submit">Liberar</button>
                </form>
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p>Não há cadastros pendentes.</p>
        {% endif %}
        <a href="/login" class="btn-neon">Sair</a>
    </div>
</body>
</html>
''',

    "static/neon.css": '''
body.bg-neon {
    background: #181A20;
    color: #fff;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.container-neon {
    max-width: 340px;
    margin: 60px auto;
    padding: 2em 2em 2em 2em;
    border-radius: 15px;
    background: rgba(24,26,32,0.93);
    box-shadow: 0 0 32px #07f8d9, 0 0 8px #181A20;
}
.title-neon {
    text-align: center;
    margin-bottom: 1em;
    color: #07f8d9;
    text-shadow: 0 0 10px #07f8d9, 0 0 6px #181A20;
}
.form-neon input[type="text"],
.form-neon input[type="password"] {
    width: 100%;
    padding: 0.75em;
    margin-bottom: 1em;
    border: none;
    border-radius: 7px;
    background: #2c2f37;
    color: #fff;
    font-size: 1em;
}
.form-neon .btn-neon {
    width: 100%;
    padding: 0.8em;
    background: #07f8d9;
    color: #181A20;
    font-weight: bold;
    border: none;
    border-radius: 7px;
    box-shadow: 0 0 8px #07f8d9, 0 0 2px #181A20;
    cursor: pointer;
    font-size: 1.08em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    transition: 0.2s;
}
.form-neon .btn-neon:hover {
    background: #24fff8;
    box-shadow: 0 0 24px #07f8d9;
}
.links-neon {
    text-align: center;
    margin-top: 1em;
}
.links-neon a {
    color: #07f8d9;
    text-decoration: none;
}
.form-row {
    margin-bottom: 0.7em;
    display: flex;
    align-items: center;
    gap: 0.4em;
}
.msg-neon {
    background: #1a2d2a;
    color: #07f8d9;
    border-radius: 8px;
    text-align: center;
    margin-top: 1.2em;
    padding: 0.8em 0.4em;
    box-shadow: 0 0 8px #07f8d9;
    animation: fadeout 3.5s forwards;
}
@keyframes fadeout {
    0% { opacity: 1; }
    80% { opacity: 1;}
    100% { opacity: 0;}
}
'''
}

# Criação dos arquivos
for path, content in files.items():
    full_path = os.path.join(ROOT, path)
    # Cria subpastas se necessário
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("\nProjeto SocialMaster MVP criado com sucesso!")
print("Siga as instruções abaixo para rodar:\n")
print("1. Ative seu ambiente conda:")
print("   conda activate socialmaster")
print("2. Instale as dependências:")
print("   pip install -r requirements.txt")
print("3. Inicialize o banco de dados:")
print("   python db_init.py")
print("4. Rode o servidor:")
print("   uvicorn main:app --reload")
print("\nAcesse http://localhost:8000/login no navegador.")
