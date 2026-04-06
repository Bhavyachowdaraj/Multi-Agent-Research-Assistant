@echo off
echo.
echo   NEXUS AI - Setup and Launch
echo ============================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install Python 3.9+ from python.org
    pause
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting Nexus AI on http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py
pause
