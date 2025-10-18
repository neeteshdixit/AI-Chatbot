# 🚀 MindMate - Quick Start Guide

## ⚡ 3-Step Setup (First Time)

### Step 1: Install Dependencies

```bash
# Run the setup script
setup_project.bat
```

This will:
- Create Python virtual environment
- Install Python packages
- Install Node.js packages

---

### Step 2: Train Models (30-60 minutes)

**Train Emotion Detector** (~15-30 min)
```bash
venv\Scripts\activate
python train_emotion.py
```

**Train Response Generator** (~15-30 min)
```bash
python fine_tune.py
```

✅ **Both models must be trained before running the app!**

---

### Step 3: Start Application

```bash
# Simply run this:
start_all.bat
```

Or manually:

**Terminal 1 - Backend:**
```bash
venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🌐 Access Points

- **Main App**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🧪 Quick Test

1. Open http://localhost:3000
2. Click "I Understand, Continue" on disclaimer
3. Type: "I'm feeling happy today!"
4. Check if emotion "joy" is detected
5. Try: "I'm feeling sad" → should detect "sadness"

---

## 📁 Project Structure

```
AI-ChatBot/
├── app.py                    ← Backend server
├── train_emotion.py          ← Train emotion model
├── fine_tune.py             ← Train response model
├── crisis_detector.py       ← Crisis detection logic
├── models/                  ← Trained models (after training)
│   ├── emotion_detector/
│   └── response_model/
└── frontend/                ← React frontend
    ├── src/
    │   ├── App.jsx          ← Main UI component
    │   ├── App.css
    │   └── index.css
    └── package.json
```

---

## 🎯 Common Commands

### Backend
```bash
# Activate environment
venv\Scripts\activate

# Start server
uvicorn app:app --host 0.0.0.0 --port 8000

# Run tests
python test_api.py

# Evaluate models
python evaluate.py
```

### Frontend
```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## ❓ Troubleshooting

### "Models not found" error
```bash
# Train the models first:
python train_emotion.py
python fine_tune.py
```

### Port already in use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend won't connect to backend
- Ensure backend is running on port 8000
- Check `frontend/vite.config.js` proxy settings
- Try restarting both servers

### Slow responses
- Normal on CPU (1-2 seconds)
- Use GPU for faster inference
- Check RAM usage (need 4GB+ free)

---

## 🔑 Key Features to Test

1. **Emotion Detection**: Try happy, sad, angry messages
2. **Crisis Detection**: Type "I'm feeling hopeless" (safe test)
3. **Memory**: Ask follow-up questions
4. **UI**: Check emoji indicators, colors, timestamps

---

## 📚 Documentation

- **Full README**: `README.md`
- **Testing Guide**: `TEST_GUIDE.md`
- **Architecture**: `ARCHITECTURE.md`
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🆘 Support Resources

### Mental Health Helplines
- **India**: AASRA - 91-9820466726 (24/7)
- **USA**: 988 (Suicide & Crisis Lifeline)
- **UK**: 116 123 (Samaritans)

### Project Help
- Check `FAQ.md` for common questions
- Review logs in terminal for errors
- Open browser DevTools (F12) for frontend issues

---

## ✅ Success Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Both models trained
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can send messages and get responses
- [ ] Emotions are detected correctly
- [ ] UI looks clean and modern

---

## 🎓 For PBL Demo

1. **Preparation**:
   - Ensure both servers are running
   - Open app in browser
   - Prepare test messages
   - Have a second screen/tab with code ready

2. **Demo Flow**:
   - Show disclaimer
   - Test normal conversation
   - Demonstrate emotion detection
   - Show crisis detection (carefully)
   - Highlight conversation memory
   - Show code architecture

3. **Q&A Prep**:
   - Know your accuracy metrics (run `evaluate.py`)
   - Understand model architecture
   - Be ready to explain crisis detection logic
   - Have limitations ready (English only, etc.)

---

**Built with ❤️ for mental health awareness**

*Remember: This is a learning project. For real mental health support, always consult licensed professionals.*
