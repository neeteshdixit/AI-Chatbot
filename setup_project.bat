@echo off
echo ========================================
echo  MindMate - Project Setup Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b 1
)
python --version
echo.

echo [2/4] Setting up Python virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

echo [3/4] Installing Python dependencies...
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Python dependencies installed
echo.

echo [4/4] Setting up Frontend...
cd frontend
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 18+
    cd ..
    pause
    exit /b 1
)
node --version
npm --version
echo.

echo Installing frontend dependencies...
if not exist "node_modules" (
    npm install
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] Frontend dependencies already installed
)
cd ..
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Train models (if not done):
echo      python train_emotion.py
echo      python fine_tune.py
echo.
echo   2. Start the application:
echo      start_all.bat
echo.
pause
