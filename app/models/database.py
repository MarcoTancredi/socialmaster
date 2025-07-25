"""
🚀 SocialMaster Database Models - Complete Architecture
Team: Anthropic NEXUS - Competition Day 1

COMPLETE DATABASE SYSTEM:
✅ Users table with admin user 'goofy'
✅ Log table for comprehensive audit trail
✅ Config table with rate limiting settings
✅ Clients table for user's social media clients
✅ Posts table for scheduled social media posts
✅ Rate limiting system (LoginFailsNew, LoginNewDeltaTime, LoginNewTimeout)
✅ IP tracking and blocking functionality
✅ Admin authentication system
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import hashlib
import json

Base = declarative_base()

class User(Base):
    """
    Users table with complete authentication system
    Includes rate limiting and admin functionality
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(50), unique=True, nullable=False, index=True)
    company = Column(String(100))
    phone = Column(String(20))  # Format: +55 11 9999-9999 or +1 555 999-9999
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    class_level = Column(String(5), default="00000")  # 5 chars: email, SMS, WhatsApp, consent, admin
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    last_used_at = Column(DateTime)
    last_accessed_ip = Column(String(45))  # IPv6 compatible
    
    # Relationships
    clients = relationship("Client", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="user")

class Log(Base):
    """
    Comprehensive audit logging for all system actions
    Required for competition - everything must be audited
    """
    __tablename__ = "log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for system logs
    ip = Column(String(45), nullable=False)
    timestamp = Column(DateTime, default=func.now(), index=True)
    description = Column(Text, nullable=False)
    action_type = Column(String(50), index=True)  # login, logout, create, update, delete, etc.
    details = Column(Text)  # JSON string for additional details
    
    # Relationships
    user = relationship("User", back_populates="logs")

class Config(Base):
    """
    System configuration table
    Default values: LoginFailsNew=5, LoginNewDeltaTime=600, LoginNewTimeout=600
    """
    __tablename__ = "config"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    variable = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Client(Base):
    """
    Client management - each user can have multiple clients
    Each client can publish to multiple social media platforms
    """
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    description = Column(Text)
    social_platforms = Column(Text)  # JSON: ["facebook", "instagram", "twitter", "linkedin", "tiktok"]
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="clients")
    posts = relationship("Post", back_populates="client", cascade="all, delete-orphan")

class Post(Base):
    """
    Social media posts scheduling and management
    Supports multiple platforms per post
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    content = Column(Text, nullable=False)
    platforms = Column(Text, nullable=False)  # JSON: ["facebook", "instagram"]
    scheduled_time = Column(DateTime, nullable=False, index=True)
    status = Column(String(20), default="scheduled", index=True)  # scheduled, published, failed
    created_at = Column(DateTime, default=func.now())
    published_at = Column(DateTime)
    error_message = Column(Text)
    media_urls = Column(Text)  # JSON: ["url1", "url2"] for images/videos
    
    # Relationships
    client = relationship("Client", back_populates="posts")

class DatabaseManager:
    """
    Database management class with initialization and helper methods
    """
    def __init__(self, database_url="sqlite:///socialmaster.db"):
        self.engine = create_engine(database_url, echo=False)  # Set echo=True for debugging
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        print("✅ All database tables created successfully!")
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
        
    def init_default_data(self):
        """
        Initialize default configuration and admin user
        Creates admin user 'goofy' with password '8569658Zz!.'
        """
        session = self.get_session()
        try:
            # Create default configuration values
            default_configs = [
                ("LoginFailsNew", "5", "Maximum login attempts for new users"),
                ("LoginNewDeltaTime", "600", "Time window for login attempts (seconds)"),
                ("LoginNewTimeout", "600", "IP block timeout (seconds)"),
                ("MaxUsersPerIP", "5", "Maximum user registrations per IP per time window"),
                ("RegistrationEnabled", "true", "Enable user registration"),
                ("MaintenanceMode", "false", "System maintenance mode"),
                ("MaxClientsPerUser", "10", "Maximum clients per user"),
                ("MaxPostsPerDay", "100", "Maximum posts per day per user")
            ]
            
            for variable, value, description in default_configs:
                existing = session.query(Config).filter(Config.variable == variable).first()
                if not existing:
                    config = Config(variable=variable, value=value, description=description)
                    session.add(config)
                    print(f"📝 Added config: {variable} = {value}")
            
            # Create admin user 'goofy' as specified
            existing_admin = session.query(User).filter(User.user == "goofy").first()
            if not existing_admin:
                # Hash password: 8569658Zz!.
                password_hash = hashlib.sha256("8569658Zz!.".encode('utf-8')).hexdigest()
                
                admin_user = User(
                    user="goofy",
                    email="goofy@acme.com",
                    company="Acme",
                    password_hash=password_hash,
                    class_level="99999",  # Super admin (5th character = 9)
                    is_active=True,
                    last_accessed_ip="127.0.0.1",
                    last_used_at=datetime.now()
                )
                session.add(admin_user)
                print("👤 Created admin user: goofy@acme.com")
                
                # Log admin creation
                log_entry = Log(
                    user_id=None,  # System log
                    ip="127.0.0.1",
                    description="Admin user 'goofy' created during system initialization",
                    action_type="admin_creation",
                    details=json.dumps({
                        "user": "goofy", 
                        "email": "goofy@acme.com", 
                        "company": "Acme",
                        "created_by": "NEXUS_SYSTEM"
                    })
                )
                session.add(log_entry)
            
            session.commit()
            print("✅ Default data initialized successfully!")
            print("🔑 Admin credentials: goofy@acme.com / 8569658Zz!.")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error initializing default data: {e}")
            raise
        finally:
            session.close()

# Authentication and security helper functions
def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == password_hash

def hash_password(password: str) -> str:
    """Hash password for storage"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_user_by_email(email: str, session):
    """Get user by email address"""
    return session.query(User).filter(User.email == email).first()

def get_user_by_username(username: str, session):
    """Get user by username"""
    return session.query(User).filter(User.user == username).first()

def is_admin_user(user: User) -> bool:
    """Check if user is admin (5th character >= 5)"""
    if not user or len(user.class_level) < 5:
        return False
    return int(user.class_level[4]) >= 5

def is_super_admin(user: User) -> bool:
    """Check if user is super admin (5th character = 9)"""
    if not user or len(user.class_level) < 5:
        return False
    return user.class_level[4] == '9'

def log_action(user_id: int, ip: str, description: str, action_type: str, details: dict = None, session=None):
    """
    Log user action with comprehensive audit trail
    Required for competition - all actions must be logged
    """
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        log_entry = Log(
            user_id=user_id,
            ip=ip,
            description=description,
            action_type=action_type,
            details=json.dumps(details) if details else None
        )
        session.add(log_entry)
        session.commit()
        print(f"📝 Logged: {action_type} - {description}")
    except Exception as e:
        session.rollback()
        print(f"❌ Logging error: {e}")
    finally:
        if should_close_session:
            session.close()

def get_config_value(variable: str, default: str = None, session=None):
    """Get configuration value"""
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        config = session.query(Config).filter(Config.variable == variable).first()
        return config.value if config else default
    finally:
        if should_close_session:
            session.close()

def set_config_value(variable: str, value: str, description: str = None, session=None):
    """Set configuration value"""
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        config = session.query(Config).filter(Config.variable == variable).first()
        if config:
            config.value = value
            config.updated_at = datetime.now()
            if description:
                config.description = description
        else:
            config = Config(variable=variable, value=value, description=description)
            session.add(config)
        session.commit()
        print(f"⚙️ Config updated: {variable} = {value}")
    except Exception as e:
        session.rollback()
        print(f"❌ Config update error: {e}")
    finally:
        if should_close_session:
            session.close()

def check_rate_limit(ip: str, action_type: str, session=None):
    """
    Check if IP is rate limited for specific action
    Implementation of LoginFailsNew, LoginNewDeltaTime, LoginNewTimeout
    
    Returns: (allowed: bool, remaining_attempts: int, time_until_reset: int)
    """
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        # Get rate limit configuration
        max_attempts = int(get_config_value("LoginFailsNew", "5", session))
        time_window = int(get_config_value("LoginNewDeltaTime", "600", session))
        
        # Count recent attempts in time window
        time_threshold = datetime.now() - timedelta(seconds=time_window)
        recent_attempts = session.query(Log).filter(
            Log.ip == ip,
            Log.action_type == action_type,
            Log.timestamp >= time_threshold
        ).count()
        
        allowed = recent_attempts < max_attempts
        remaining = max(0, max_attempts - recent_attempts)
        
        if not allowed:
            # Log rate limit hit
            log_action(
                None, ip, f"Rate limit exceeded for {action_type}", 
                "rate_limit_exceeded",
                {"attempts": recent_attempts, "max_attempts": max_attempts},
                session
            )
        
        return allowed, remaining, time_window
        
    finally:
        if should_close_session:
            session.close()

def is_ip_blocked(ip: str, session=None):
    """
    Check if IP is currently blocked due to rate limiting
    """
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        timeout_seconds = int(get_config_value("LoginNewTimeout", "600", session))
        time_threshold = datetime.now() - timedelta(seconds=timeout_seconds)
        
        # Check for recent rate limit violations
        recent_blocks = session.query(Log).filter(
            Log.ip == ip,
            Log.action_type == "rate_limit_exceeded",
            Log.timestamp >= time_threshold
        ).count()
        
        return recent_blocks > 0
        
    finally:
        if should_close_session:
            session.close()

def create_client(user_id: int, name: str, email: str, description: str, platforms: list, session=None):
    """Create new client for user"""
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        client = Client(
            user_id=user_id,
            name=name,
            email=email,
            description=description,
            social_platforms=json.dumps(platforms)
        )
        session.add(client)
        session.commit()
        
        log_action(
            user_id, "system", f"Created client: {name}",
            "client_created",
            {"client_name": name, "client_email": email, "platforms": platforms},
            session
        )
        
        return client
        
    except Exception as e:
        session.rollback()
        print(f"❌ Client creation error: {e}")
        return None
    finally:
        if should_close_session:
            session.close()

def schedule_post(client_id: int, content: str, platforms: list, scheduled_time: datetime, media_urls: list = None, session=None):
    """Schedule social media post"""
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        post = Post(
            client_id=client_id,
            content=content,
            platforms=json.dumps(platforms),
            scheduled_time=scheduled_time,
            media_urls=json.dumps(media_urls) if media_urls else None
        )
        session.add(post)
        session.commit()
        
        # Get client info for logging
        client = session.query(Client).filter(Client.id == client_id).first()
        if client:
            log_action(
                client.user_id, "system", f"Scheduled post for client: {client.name}",
                "post_scheduled",
                {
                    "client_name": client.name,
                    "platforms": platforms,
                    "scheduled_time": scheduled_time.isoformat(),
                    "content_length": len(content)
                },
                session
            )
        
        return post
        
    except Exception as e:
        session.rollback()
        print(f"❌ Post scheduling error: {e}")
        return None
    finally:
        if should_close_session:
            session.close()

def get_pending_posts(session=None):
    """Get posts that are ready to be published"""
    should_close_session = session is None
    if session is None:
        db = DatabaseManager()
        session = db.get_session()
    
    try:
        now = datetime.now()
        pending_posts = session.query(Post).filter(
            Post.status == "scheduled",
            Post.scheduled_time <= now
        ).all()
        
        return pending_posts
        
    finally:
        if should_close_session:
            session.close()

# Database initialization function
def init_database():
    """
    Initialize complete database system
    Call this function to set up SocialMaster database
    """
    print("🚀 SocialMaster Database Initialization")
    print("=" * 50)
    
    db = DatabaseManager()
    
    print("📊 Creating database tables...")
    db.create_tables()
    
    print("📝 Initializing default data and admin user...")
    db.init_default_data()
    
    print("🔍 Verifying database setup...")
    session = db.get_session()
    try:
        user_count = session.query(User).count()
        config_count = session.query(Config).count()
        admin_user = session.query(User).filter(User.user == "goofy").first()
        
        print(f"👥 Users in database: {user_count}")
        print(f"⚙️ Config entries: {config_count}")
        print(f"👤 Admin user active: {'✅' if admin_user and admin_user.is_active else '❌'}")
        
        if admin_user:
            print(f"🔑 Admin access level: {admin_user.class_level}")
            print(f"📧 Admin email: {admin_user.email}")
    
    finally:
        session.close()
    
    print("✅ Database initialization complete!")
    print("🏆 Team Anthropic NEXUS - Ready for competition!")
    return db

# Main execution
if __name__ == "__main__":
    print("🤖 NEXUS Database System - SocialMaster")
    print("Team: Anthropic NEXUS")
    print("Competition: Social Media Automation Platform")
    print("=" * 60)
    
    # Initialize database
    database = init_database()
    
    print("\n🎯 Database Features:")
    print("✅ User management with admin controls")
    print("✅ Comprehensive audit logging")
    print("✅ Rate limiting and IP blocking")
    print("✅ Client and social media management")
    print("✅ Post scheduling system")
    print("✅ Configuration management")
    
    print("\n🔑 Default Admin Credentials:")
    print("Username: goofy")
    print("Email: goofy@acme.com")
    print("Password: 8569658Zz!.")
    print("Access Level: Super Admin (99999)")
    
    print("\n⚙️ Rate Limiting Settings:")
    print("LoginFailsNew: 5 attempts")
    print("LoginNewDeltaTime: 600 seconds")
    print("LoginNewTimeout: 600 seconds")
    
    print("\n🚀 Ready for SocialMaster application integration!")
    print("💪 NEXUS automation system operational!")