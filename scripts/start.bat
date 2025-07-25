@echo off
title SocialMaster Platform - Team Anthropic NEXUS
echo ================================================
echo        🚀 SOCIALMASTER PLATFORM
echo        Team: Anthropic NEXUS
echo        Competition Day: 1
echo ================================================
echo.

REM Ativar ambiente conda (se usando)
if exist "%CONDA_DEFAULT_ENV%" (
    call conda activate social_platform
)

REM Verificar se estamos na pasta correta
if not exist "app\main.py" (
    echo ❌ ERRO: Execute este script na pasta raiz do SocialMaster
    echo Pasta atual: %CD%
    pause
    exit /b 1
)

echo ✅ SocialMaster environment ready!
echo.

REM Instalar dependências se necessário
if exist "requirements.txt" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Iniciar aplicação
echo 🚀 Starting SocialMaster Platform...
echo.
echo 📱 Access URLs:
echo    Main App: http://localhost:8000
echo    API Docs: http://localhost:8000/api/docs
echo    Health:   http://localhost:8000/health
echo.
echo ⏹️  To stop: Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause