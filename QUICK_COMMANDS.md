# Quick Commands Reference

## ✅ Issues Fixed

1. ✅ Installed `scikit-learn` for emotion training
2. ✅ Installed frontend dependencies from correct directory

---

## 🚀 Correct Commands

### Backend Setup & Training

```bash
# Install Python dependencies (from root directory)
pip install -r requirements.txt

# Train emotion model (~30 min on GPU, 2-3 hours on CPU)
python train_emotion.py

# Train response model (~1 hour on GPU, 4-6 hours on CPU)
python fine_tune.py

# Start backend server
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend Setup & Start

```bash
# IMPORTANT: Navigate to frontend directory first!
cd frontend

# Install dependencies (one-time)
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Testing

```bash
# From root directory
python test_api.py
python demo_script.py
python run_tests.py
```

---

## ⚠️ Common Mistakes

### ❌ WRONG: Running npm from root directory
```bash
# This will fail!
npm install          # No package.json in root
npm run dev          # No package.json in root
```

### ✅ CORRECT: Running npm from frontend directory
```bash
cd frontend
npm install          # Works!
npm run dev          # Works!
```

---

## 🎯 Quick Start (Without Training)

If you want to test the system without waiting for training:

### Terminal 1: Backend
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Browser
```
http://localhost:3000
```

**Note:** The system will use base (untrained) models, which still work but may be less accurate.

---

## 📊 Current Status

✅ **scikit-learn** - Installed  
✅ **Frontend dependencies** - Installed  
🔄 **Emotion model training** - Running in background  
⏳ **Response model training** - Not started yet  

---

## 🔄 Training Progress

### Emotion Model (train_emotion.py)
- **Dataset:** dair-ai/emotion (16,000 training samples)
- **Model:** BERT-base-uncased
- **Time:** ~30 min on GPU, 2-3 hours on CPU
- **Output:** `./models/emotion_model/`

### Response Model (fine_tune.py)
- **Dataset:** empathetic_dialogues
- **Model:** DialoGPT-medium
- **Time:** ~1 hour on GPU, 4-6 hours on CPU
- **Output:** `./models/response_model/`

---

## 💡 Pro Tips

1. **Training is Optional:** The system works with base models if you skip training
2. **Use GPU if Available:** Training is much faster on GPU
3. **Monitor Training:** Check terminal output for progress
4. **Test First:** Run `python test_api.py` to verify setup before training
5. **Frontend First:** Start frontend to see the UI while backend trains

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
pip install X
# or
pip install -r requirements.txt
```

### "npm error ENOENT: no such file or directory, open 'package.json'"
```bash
# You're in the wrong directory!
cd frontend
npm install
```

### "Port 8000 already in use"
```bash
# Kill existing process or use different port
uvicorn app:app --host 0.0.0.0 --port 8001
```

### "Port 3000 already in use"
```bash
# Vite will automatically suggest port 3001
# Or specify manually in vite.config.js
```

---

## 📝 Next Steps

1. **Wait for training to complete** (or skip and use base models)
2. **Start backend:** `uvicorn app:app --host 0.0.0.0 --port 8000`
3. **Start frontend:** `cd frontend && npm run dev`
4. **Test the chatbot:** Open http://localhost:3000
5. **Try crisis detection:** Type "I want to end my life"

---

**Last Updated:** 2024-10-12  
**Status:** Ready to run!
