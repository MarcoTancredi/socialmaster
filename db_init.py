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
