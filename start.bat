@echo off
REM MindMate Chatbot Startup Script for Windows
REM This script starts both backend and frontend servers

echo ========================================
echo    MindMate Chatbot - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if models exist
if not exist "models\emotion_detector" (
    echo [WARNING] Emotion model not found at models\emotion_detector
    echo The chatbot will use the base BERT model instead.
    echo For better performance, train the model first:
    echo   python train_emotion.py
    echo.
)

if not exist "models\response_model" (
    echo [WARNING] Response model not found at models\response_model
    echo The chatbot will use the base DialoGPT model instead.
    echo For better performance, train the model first:
    echo   python fine_tune.py
    echo.
)

echo [1/2] Starting Backend Server...
echo.
start "MindMate Backend" cmd /k "venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 5 /nobreak > nul

echo [2/2] Starting Frontend Server...
echo.
cd frontend
start "MindMate Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo    MindMate is starting up!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop the servers.
echo.
pause
