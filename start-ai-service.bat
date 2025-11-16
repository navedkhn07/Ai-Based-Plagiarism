@echo off
echo Starting AI Service...
echo.
cd ai-service
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Starting AI Service on http://localhost:8000
echo.
python app.py
pause

