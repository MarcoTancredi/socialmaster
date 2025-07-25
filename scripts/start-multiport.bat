@echo off
title SocialMaster Multi-Port - Team Anthropic NEXUS
echo ================================================
echo     🚀 SOCIALMASTER MULTI-PORT STARTUP
echo     Team: Anthropic NEXUS - Competition Day 1
echo ================================================
echo.

REM Ativar ambiente conda
call conda activate socialmaster

REM Verificar CloudFlare tunnel
echo 🌐 Checking CloudFlare tunnel status...
cloudflared tunnel list

echo.
echo 🚀 Starting SocialMaster Multi-Port Architecture...
echo.
echo 📱 Frontend:  https://app.planetamicro.com.br
echo 🔌 API:       https://api.planetamicro.com.br  
echo 🔐 Admin:     https://admin.planetamicro.com.br
echo 📊 Monitor:   https://monitor.planetamicro.com.br
echo.

REM Iniciar aplicações em paralelo
start "Frontend-8000" cmd /k "conda activate socialmaster && python -c "from app.main import main_app; import uvicorn; uvicorn.run(main_app, host='0.0.0.0', port=8000)""

start "API-8001" cmd /k "conda activate socialmaster && python -c "from app.main import api_app; import uvicorn; uvicorn.run(api_app, host='0.0.0.0', port=8001)""

start "Admin-8002" cmd /k "conda activate socialmaster && python -c "from app.main import admin_app; import uvicorn; uvicorn.run(admin_app, host='0.0.0.0', port=8002)""

start "Monitor-8003" cmd /k "conda activate socialmaster && python -c "from app.main import monitor_app; import uvicorn; uvicorn.run(monitor_app, host='0.0.0.0', port=8003)""

echo ✅ All services starting...
echo 🌐 CloudFlare tunnels should route traffic automatically
echo.
pause