from models import Base, engine, SessionLocal, User, ConfigVar
from passlib.hash import bcrypt

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Admin user
    if not db.query(User).filter_by(user="goofy").first():
        admin = User(
            user="goofy",
            company="Acme",
            phone="localhost",
            email="goofy@acme.com",
            password_hash=bcrypt.hash("8569658Zz!."),
            class_field="99999",
            is_active=True
        )
        db.add(admin)
        db.commit()
    # Config vars
    defaults = [
        ("LoginFailsNew", "5"),
        ("LogINNewDeltaTime", "600"),
        ("LoginINNewTimeout", "600"),
    ]
    for k, v in defaults:
        if not db.query(ConfigVar).filter_by(variable=k).first():
            db.add(ConfigVar(variable=k, value=v))
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized.")
