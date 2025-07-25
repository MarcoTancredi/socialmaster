from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    class_field = Column(String(5), default="00000")
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    last_used_at = Column(DateTime, default=datetime.now)
    last_accessed_ip = Column(String, nullable=True)

class ConfigVar(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True)
    variable = Column(String, unique=True)
    value = Column(String)

DATABASE_URL = "sqlite:///./socialmaster.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
