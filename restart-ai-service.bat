@echo off
echo Stopping any existing AI service...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting AI Service...
cd ai-service
python app.py

