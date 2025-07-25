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
