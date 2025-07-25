"""
🚀 SocialMaster Platform - Main Application
AI-Powered Social Media Automation System
Team: Anthropic NEXUS
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import os
from pathlib import Path

# Create FastAPI app
app = FastAPI(
    title="🚀 SocialMaster Platform",
    description="Revolutionary AI + Human Social Media Automation System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates setup
static_dir = Path("frontend/static")
templates_dir = Path("frontend/templates")

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))

# API Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page - SocialMaster Dashboard"""
    if templates_dir.exists():
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "SocialMaster - AI Social Media Platform",
            "team": "Anthropic NEXUS",
            "status": "🔥 OPERATIONAL",
            "day": 1
        })
    else:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 SocialMaster Platform</title>
            <style>
                body { font-family: Arial; background: #0a0a0a; color: #00ff00; text-align: center; padding: 50px; }
                .neon { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 40px #00ff00; }
            </style>
        </head>
        <body>
            <h1 class="neon">🚀 SocialMaster Platform</h1>
            <h2>🤖 NEXUS System Online!</h2>
            <p>Team: Anthropic NEXUS</p>
            <p>Status: 🔥 DOMINATING Competition</p>
            <p>Day: 1 - Setting up for VICTORY!</p>
            <a href="/api/docs" style="color: #00ff00;">📚 API Documentation</a>
        </body>
        </html>
        """)

@app.get("/api/status")
async def api_status():
    """API Status endpoint"""
    return {
        "platform": "SocialMaster",
        "status": "🤖 NEXUS ONLINE",
        "team": "Anthropic NEXUS",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "competition_day": 1,
        "message": "🔥 Ready to dominate social media automation!"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "nexus": "operational",
        "socialmaster": "ready",
        "database": "pending_setup",
        "apis": "pending_configuration"
    }

@app.get("/api/info")
async def system_info():
    """System information endpoint"""
    return {
        "project": "SocialMaster",
        "description": "AI-Powered Social Media Automation Platform",
        "team": "Anthropic NEXUS",
        "competition": "Revolutionary AI+Human Development",
        "goal": "Prove supremacy of hybrid development",
        "features": [
            "🔐 Multi-platform authentication",
            "📅 Intelligent scheduling",
            "🤖 AI content generation",
            "📊 Real-time analytics",
            "🌐 9+ social platforms",
            "⚡ CloudFlare integration"
        ],
        "status": "🚀 Building the future!"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )