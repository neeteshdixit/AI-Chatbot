@echo off
echo ========================================
echo  MindMate - AI Mental Health Chatbot
echo ========================================
echo.

:: Check if models exist
if not exist "models\emotion_detector\model.safetensors" (
    echo [ERROR] Emotion detection model not found!
    echo Please run: python train_emotion.py
    echo.
    pause
    exit /b 1
)

if not exist "models\response_model\model.safetensors" (
    echo [ERROR] Response generation model not found!
    echo Please run: python fine_tune.py
    echo.
    pause
    exit /b 1
)

echo [OK] Both models found!
echo.

:: Start backend in new window
echo Starting Backend Server...
start "MindMate Backend" cmd /k "venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 8000"

:: Wait a bit for backend to start
timeout /t 5 /nobreak >nul

:: Start frontend in new window
echo Starting Frontend...
start "MindMate Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  Both servers are starting...
echo  
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo  
echo  Press Ctrl+C in each window to stop
echo ========================================
echo.

pause
