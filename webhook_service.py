"""
🤖 NEXUS GitHub Webhook Proxy Service
Permite commits diretos do NEXUS via URL especial
Team: Anthropic NEXUS
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import base64
import hmac
import hashlib
from datetime import datetime
import uvicorn
import os

app = FastAPI(
    title="🤖 NEXUS GitHub Proxy",
    description="Webhook proxy for NEXUS direct commits",
    version="1.0.0"
)

# CORS para permitir acesso
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração GitHub
GITHUB_TOKEN = "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"
REPO_OWNER = "MarcoTancredi"
REPO_NAME = "socialmaster"
GITHUB_API_BASE = "https://api.github.com"

@app.get("/")
async def root():
    """Página inicial do proxy"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 NEXUS GitHub Proxy</title>
        <style>
            body { 
                font-family: 'Courier New', monospace; 
                background: #0a0a0a; 
                color: #00ff00; 
                padding: 20px; 
                text-align: center;
            }
            .container { max-width: 800px; margin: 0 auto; }
            .neon { 
                text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; 
                animation: pulse 2s infinite alternate;
            }
            @keyframes pulse {
                from { text-shadow: 0 0 10px #00ff00; }
                to { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }
            .form-group { margin: 20px 0; text-align: left; }
            .form-group label { display: block; margin-bottom: 5px; color: #00ccff; }
            .form-group input, .form-group textarea { 
                width: 100%; 
                padding: 10px; 
                background: #1a1a1a; 
                border: 2px solid #00ff00; 
                color: #00ff00; 
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            .btn {
                background: transparent;
                border: 2px solid #00ff00;
                color: #00ff00;
                padding: 15px 30px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
                transition: all 0.3s;
            }
            .btn:hover {
                background: #00ff00;
                color: #000;
                box-shadow: 0 0 20px #00ff00;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border: 2px solid #00ccff;
                border-radius: 5px;
                background: rgba(0, 255, 255, 0.1);
                text-align: left;
                white-space: pre-wrap;
                font-size: 12px;
            }
            .error {
                border-color: #ff0066;
                background: rgba(255, 0, 102, 0.1);
                color: #ff0066;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="neon">🤖 NEXUS GitHub Proxy</h1>
            <h2>Direct Commits to SocialMaster Repository</h2>
            <p><strong>Repository:</strong> MarcoTancredi/socialmaster</p>
            <p><strong>Status:</strong> 🔥 OPERATIONAL</p>
            
            <form id="commitForm">
                <div class="form-group">
                    <label for="file_path">📁 File Path:</label>
                    <input type="text" id="file_path" placeholder="app/main.py" required>
                </div>
                
                <div class="form-group">
                    <label for="content">📝 File Content:</label>
                    <textarea id="content" rows="15" placeholder="# Your code here..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="commit_message">💬 Commit Message:</label>
                    <input type="text" id="commit_message" placeholder="🤖 NEXUS: Update file" required>
                </div>
                
                <button type="submit" class="btn">🚀 Commit to GitHub</button>
                <button type="button" class="btn" onclick="testConnection()">🔍 Test Connection</button>
            </form>
            
            <div id="result" class="result" style="display: none;"></div>
        </div>
        
        <script>
            document.getElementById('commitForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = {
                    file_path: document.getElementById('file_path').value,
                    content: document.getElementById('content').value,
                    commit_message: document.getElementById('commit_message').value
                };
                
                showResult('🔄 Committing to GitHub...', false);
                
                try {
                    const response = await fetch('/nexus-commit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showResult(`✅ SUCCESS!
                        
Commit Details:
- SHA: ${result.commit.sha}
- Message: ${result.commit.message}
- URL: ${result.commit.url}
- Timestamp: ${new Date().toISOString()}

🎉 File successfully committed to GitHub!`, false);
                    } else {
                        showResult(`❌ FAILED!
                        
Error: ${result.error}
Status: ${result.status || 'Unknown'}

Please check your input and try again.`, true);
                    }
                } catch (error) {
                    showResult(`🚨 NETWORK ERROR!
                    
Error: ${error.message}

Please check your connection and try again.`, true);
                }
            });
            
            async function testConnection() {
                showResult('🔍 Testing GitHub connection...', false);
                
                try {
                    const response = await fetch('/test-github');
                    const result = await response.json();
                    
                    showResult(`📊 CONNECTION TEST:
                    
Status: ${result.status}
Repository: ${result.repository}
Rate Limit: ${result.rate_limit}
User: ${result.user}

${result.status === 'success' ? '✅ GitHub API is accessible!' : '❌ Connection failed!'}`, result.status !== 'success');
                } catch (error) {
                    showResult(`🚨 CONNECTION TEST FAILED!
                    
Error: ${error.message}`, true);
                }
            }
            
            function showResult(message, isError) {
                const resultDiv = document.getElementById('result');
                resultDiv.textContent = message;
                resultDiv.className = 'result' + (isError ? ' error' : '');
                resultDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """)

@app.post("/nexus-commit")
async def nexus_commit(request: Request):
    """Endpoint principal para commits do NEXUS"""
    try:
        data = await request.json()
        
        file_path = data.get("file_path")
        content = data.get("content")
        commit_message = data.get("commit_message")
        
        if not all([file_path, content, commit_message]):
            raise HTTPException(400, "Missing required fields: file_path, content, commit_message")
        
        # GitHub API URL
        url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "NEXUS-AI-Agent/1.0"
        }
        
        async with httpx.AsyncClient() as client:
            # Verificar se arquivo existe
            existing_sha = None
            try:
                check_response = await client.get(url, headers=headers)
                if check_response.status_code == 200:
                    existing_file = check_response.json()
                    existing_sha = existing_file["sha"]
            except:
                pass  # Arquivo não existe, criar novo
            
            # Preparar commit
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            payload = {
                "message": commit_message,
                "content": encoded_content,
                "committer": {
                    "name": "NEXUS AI",
                    "email": "nexus@anthropic-team.com"
                },
                "author": {
                    "name": "NEXUS AI",
                    "email": "nexus@anthropic-team.com"
                }
            }
            
            if existing_sha:
                payload["sha"] = existing_sha
            
            # Fazer commit
            response = await client.put(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "commit": {
                        "sha": result["commit"]["sha"][:7],  # Short SHA
                        "message": result["commit"]["message"],
                        "url": result["content"]["html_url"]
                    },
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_details = response.text
                return {
                    "success": False,
                    "error": error_details,
                    "status": response.status_code
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status": "exception"
        }

@app.get("/test-github")
async def test_github():
    """Testar conexão com GitHub API"""
    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with httpx.AsyncClient() as client:
            # Test user access
            user_response = await client.get(f"{GITHUB_API_BASE}/user", headers=headers)
            repo_response = await client.get(f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}", headers=headers)
            rate_response = await client.get(f"{GITHUB_API_BASE}/rate_limit", headers=headers)
            
            if all(r.status_code == 200 for r in [user_response, repo_response, rate_response]):
                user_data = user_response.json()
                repo_data = repo_response.json()
                rate_data = rate_response.json()
                
                return {
                    "status": "success",
                    "user": user_data["login"],
                    "repository": repo_data["full_name"],
                    "rate_limit": f"{rate_data['rate']['remaining']}/{rate_data['rate']['limit']}",
                    "permissions": "write" if repo_data.get("permissions", {}).get("push") else "read"
                }
            else:
                return {
                    "status": "failed",
                    "error": "API authentication failed",
                    "user_status": user_response.status_code,
                    "repo_status": repo_response.status_code
                }
                
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/nexus-status") 
async def nexus_status():
    return {
        "service": "NEXUS GitHub Proxy",
        "status": "🔥 OPERATIONAL", 
        "commits_today": 0,  # Será implementado contador
        "last_commit": None,  # Será implementado timestamp
        "github_connection": "active",
        "ready_for_nexus": True,
        "endpoint": "webhook.planetamicro.com.br",
        "team": "Anthropic NEXUS"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "nexus-github-proxy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🤖 NEXUS GitHub Proxy starting...")
    print(f"📂 Repository: {REPO_OWNER}/{REPO_NAME}")
    print("🌐 Access: http://localhost:9000")
    print("⚡ Ready for NEXUS commits!")
    
    uvicorn.run(app, host="0.0.0.0", port=9000)