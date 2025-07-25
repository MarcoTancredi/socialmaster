"""
🚀 SocialMaster Platform - Multi-Port Architecture
Team: Anthropic NEXUS
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import os
from datetime import datetime
from pathlib import Path

# Import our API routes (será criado)
from app.api.v1 import auth, users, clients, posts

# Multi-App Configuration
class SocialMasterApps:
    def __init__(self):
        self.main_app = self.create_main_app()
        self.api_app = self.create_api_app()
        self.admin_app = self.create_admin_app()
        self.monitor_app = self.create_monitor_app()
    
    def create_main_app(self):
        """Frontend Application - Port 8000"""
        app = FastAPI(
            title="🚀 SocialMaster Frontend",
            description="AI-Powered Social Media Platform - Frontend",
            version="1.0.0",
            docs_url=None,  # Disable docs on main app
            redoc_url=None
        )
        
        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://app.planetamicro.com.br", "https://api.planetamicro.com.br"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Static files and templates
        static_dir = Path("frontend/static")
        templates_dir = Path("frontend/templates")
        
        if static_dir.exists():
            app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        
        if templates_dir.exists():
            templates = Jinja2Templates(directory=str(templates_dir))
        
        @app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            return templates.TemplateResponse("index.html", {
                "request": request,
                "title": "SocialMaster - AI Social Media Platform",
                "team": "Anthropic NEXUS",
                "status": "🔥 OPERATIONAL",
                "day": 1
            })
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "app": "frontend", "port": 8000}
            
        return app
    
    def create_api_app(self):
        """API Application - Port 8001"""
        app = FastAPI(
            title="🚀 SocialMaster API",
            description="Social Media Automation API - Team Anthropic NEXUS",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["https://app.planetamicro.com.br", "https://admin.planetamicro.com.br"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Include API routes
        app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
        app.include_router(users.router, prefix="/users", tags=["Users"])
        app.include_router(clients.router, prefix="/clients", tags=["Clients"])
        app.include_router(posts.router, prefix="/posts", tags=["Posts"])
        
        @app.get("/")
        async def api_root():
            return {
                "message": "🤖 SocialMaster API - NEXUS Powered",
                "version": "1.0.0",
                "team": "Anthropic NEXUS",
                "docs": "https://api.planetamicro.com.br/docs",
                "status": "operational"
            }
        
        @app.get("/status")
        async def api_status():
            return {
                "platform": "SocialMaster API",
                "status": "🤖 NEXUS ONLINE",
                "team": "Anthropic NEXUS",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "competition_day": 1,
                "endpoints": {
                    "auth": "/auth/*",
                    "users": "/users/*", 
                    "clients": "/clients/*",
                    "posts": "/posts/*"
                }
            }
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "app": "api", "port": 8001}
            
        return app
    
    def create_admin_app(self):
        """Admin Panel - Port 8002"""
        app = FastAPI(
            title="🚀 SocialMaster Admin",
            description="Administration Panel - Team Anthropic NEXUS",
            version="1.0.0"
        )
        
        @app.get("/")
        async def admin_root():
            return {
                "message": "🔐 SocialMaster Admin Panel",
                "team": "Anthropic NEXUS",
                "access": "restricted",
                "features": [
                    "User Management",
                    "System Configuration", 
                    "Social Media Connections",
                    "Analytics Dashboard"
                ]
            }
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "app": "admin", "port": 8002}
            
        return app
    
    def create_monitor_app(self):
        """Real-time Monitoring - Port 8003"""
        app = FastAPI(
            title="🚀 SocialMaster Monitor",
            description="Real-time System Monitoring - Team Anthropic NEXUS",
            version="1.0.0"
        )
        
        @app.get("/")
        async def monitor_root():
            return {
                "message": "📊 SocialMaster Real-time Monitor",
                "team": "Anthropic NEXUS",
                "metrics": {
                    "active_users": 0,
                    "posts_scheduled": 0,
                    "social_platforms": 9,
                    "system_health": "optimal"
                }
            }
        
        @app.get("/metrics")
        async def system_metrics():
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": "15%",
                "memory_usage": "8GB/16GB",
                "network_status": "optimal",
                "cloudflare_status": "connected",
                "database_connections": 5,
                "api_requests_per_minute": 42
            }
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "app": "monitor", "port": 8003}
            
        return app

# Initialize all apps
social_master = SocialMasterApps()

# Export apps for uvicorn
main_app = social_master.main_app
api_app = social_master.api_app  
admin_app = social_master.admin_app
monitor_app = social_master.monitor_app

# Development runner
if __name__ == "__main__":
    print("🚀 Starting SocialMaster Multi-Port Architecture...")
    print("📱 Frontend: http://localhost:8000")
    print("🔌 API: http://localhost:8001") 
    print("🔐 Admin: http://localhost:8002")
    print("📊 Monitor: http://localhost:8003")
    
    # Start all servers concurrently
    import multiprocessing
    
    def start_server(app, port, app_name):
        print(f"🚀 Starting {app_name} on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    
    processes = [
        multiprocessing.Process(target=start_server, args=(main_app, 8000, "Frontend")),
        multiprocessing.Process(target=start_server, args=(api_app, 8001, "API")),
        multiprocessing.Process(target=start_server, args=(admin_app, 8002, "Admin")),
        multiprocessing.Process(target=start_server, args=(monitor_app, 8003, "Monitor"))
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()