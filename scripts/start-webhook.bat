@echo off
title NEXUS GitHub Webhook Proxy
echo =============================================
echo     🤖 NEXUS GITHUB WEBHOOK PROXY
echo     Direct commits to SocialMaster
echo =============================================

call conda activate socialmaster

echo 🚀 Starting NEXUS GitHub Proxy...
echo 🌐 Access: http://localhost:9000
echo 📂 Repository: MarcoTancredi/socialmaster
echo.

python webhook_service.py

pause
