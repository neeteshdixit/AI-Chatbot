@echo off
echo ========================================
echo  MindMate - System Status Check
echo ========================================
echo.

echo [1/4] Checking Models...
if exist "models\emotion_detector\model.safetensors" (
    echo [OK] Emotion detector model found
) else (
    echo [X] Emotion detector model NOT found
    echo     Run: python train_emotion.py
)

if exist "models\response_model\model.safetensors" (
    echo [OK] Response generator model found
) else (
    echo [X] Response generator model NOT found
    echo     Run: python fine_tune.py
)
echo.

echo [2/4] Checking Python Environment...
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment found
) else (
    echo [X] Virtual environment NOT found
    echo     Run: python -m venv venv
)
echo.

echo [3/4] Checking Frontend Setup...
if exist "frontend\node_modules" (
    echo [OK] Frontend dependencies installed
) else (
    echo [X] Frontend dependencies NOT installed
    echo     Run: cd frontend ^&^& npm install
)
echo.

echo [4/4] Checking Running Services...

:: Check backend
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [X] Backend NOT running on port 8000
    echo     Start: uvicorn app:app --host 0.0.0.0 --port 8000
) else (
    echo [OK] Backend running on http://localhost:8000
)

:: Check frontend (basic port check)
netstat -an | findstr "3000" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [X] Frontend NOT running on port 3000
    echo     Start: cd frontend ^&^& npm run dev
) else (
    echo [OK] Frontend appears to be running on port 3000
)
echo.

echo ========================================
echo  Status check complete!
echo ========================================
echo.

pause
