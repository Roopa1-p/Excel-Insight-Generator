@echo off
echo ========================================
echo Excel-to-Insights Bot - Startup Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your API keys before running the app.
    pause
    exit /b
)

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Run the Streamlit app
echo Starting Excel-to-Insights Bot...
echo.
echo The app will open in your default browser.
echo Press Ctrl+C to stop the server.
echo.
streamlit run app.py

pause
