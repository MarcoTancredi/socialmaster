@echo off
title SocialMaster Platform - Team Anthropic NEXUS
echo ================================================
echo        🚀 SOCIALMASTER PLATFORM
echo        Team: Anthropic NEXUS
echo        Competition Day: 1  
echo ================================================
echo.

REM Verificar se estamos na pasta correta
if not exist "app\main.py" (
    echo ❌ ERRO: Execute este script na pasta raiz do SocialMaster
    echo Pasta atual: %CD%
    echo.
    echo Navegue para: D:\Bin\socialmaster
    pause
    exit /b 1
)

REM Ativar ambiente conda
echo 🐍 Ativando ambiente conda...
call conda activate socialmaster
if errorlevel 1 (
    echo ❌ ERRO: Não foi possível ativar o ambiente conda 'socialmaster'
    echo.
    echo Execute antes:
    echo conda create -n socialmaster python=3.11 -y
    echo conda activate socialmaster
    pause
    exit /b 1
)

echo ✅ Ambiente conda ativado com sucesso!
echo.

REM Verificar dependências
echo 📦 Verificando dependências...
python -c "import fastapi, uvicorn" 2>NUL
if errorlevel 1 (
    echo 📦 Instalando dependências necessárias...
    pip install fastapi uvicorn[standard] jinja2 python-multipart aiofiles
)

echo ✅ Dependências verificadas!
echo.

REM Iniciar aplicação
echo 🚀 Iniciando SocialMaster Platform...
echo.
echo 📱 Acesso Local:
echo    http://localhost:8000
echo.
echo 🌐 Acesso CloudFlare (quando configurado):
echo    https://app.planetamicro.com.br
echo    https://api.planetamicro.com.br  
echo    https://admin.planetamicro.com.br
echo    https://monitor.planetamicro.com.br
echo.
echo 📚 Documentação API: http://localhost:8000/api/docs
echo 💚 Health Check: http://localhost:8000/health
echo.
echo ⏹️  Para parar: Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause