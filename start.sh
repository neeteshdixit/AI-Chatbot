#!/bin/bash
# MindMate Chatbot Startup Script for Linux/Mac
# This script starts both backend and frontend servers

echo "========================================"
echo "   MindMate Chatbot - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if models exist
if [ ! -d "models/emotion_detector" ]; then
    echo "[WARNING] Emotion model not found at models/emotion_detector"
    echo "The chatbot will use the base BERT model instead."
    echo "For better performance, train the model first:"
    echo "  python train_emotion.py"
    echo ""
fi

if [ ! -d "models/response_model" ]; then
    echo "[WARNING] Response model not found at models/response_model"
    echo "The chatbot will use the base DialoGPT model instead."
    echo "For better performance, train the model first:"
    echo "  python fine_tune.py"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

echo "[1/2] Starting Backend Server..."
echo ""
uvicorn app:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

echo "[2/2] Starting Frontend Server..."
echo ""
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "   MindMate is running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers."
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
