# 🎯 Getting Started with MindMate

Welcome to MindMate! This guide will help you get the chatbot running on your machine.

---

## 📋 What You Need

Before starting, make sure you have:

- ✅ **Python 3.10 or higher** - [Download here](https://www.python.org/downloads/)
- ✅ **Node.js 18 or higher** - [Download here](https://nodejs.org/)
- ✅ **8GB+ RAM** (16GB recommended for training)
- ✅ **10GB+ free disk space**
- ✅ **Internet connection** (for downloading models and datasets)

---

## 🚀 Three Ways to Get Started

### Option 1: Quick Start (Recommended for Testing)

**Time: 5 minutes** | Uses pre-trained base models

```bash
# 1. Setup Python environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backend (downloads base models automatically)
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open a new terminal:

```bash
# 4. Setup frontend
cd frontend
npm install
npm run dev

# 5. Open browser at http://localhost:3000
```

**Note:** First run downloads ~1GB of models. Be patient!

---

### Option 2: Full Setup with Fine-tuned Models

**Time: 2-4 hours** | Best performance for PBL project

```bash
# 1. Setup Python environment (same as Option 1)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Train emotion detection model (~30 min on GPU, 1-2 hours on CPU)
python train_emotion.py

# 3. Train response generation model (~1 hour on GPU, 2-4 hours on CPU)
python fine_tune.py

# 4. Start backend
uvicorn app:app --host 0.0.0.0 --port 8000

# 5. Setup and start frontend (in new terminal)
cd frontend
npm install
npm run dev

# 6. Open http://localhost:3000
```

---

### Option 3: Using Startup Scripts

**Time: 5 minutes** | Automated startup

**Windows:**
```bash
# First time setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd frontend
npm install
cd ..

# Then use startup script
start.bat
```

**Linux/Mac:**
```bash
# First time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend
npm install
cd ..

# Then use startup script
chmod +x start.sh
./start.sh
```

---

## ✅ Verify Installation

### 1. Check Backend

Open browser: http://localhost:8000/health

Expected response: `{"status":"ok"}`

### 2. Check Frontend

Open browser: http://localhost:3000

You should see:
- Disclaimer modal
- MindMate chat interface
- Welcome message from bot

### 3. Test Functionality

Try these messages:

| Message | Expected Behavior |
|---------|------------------|
| "Hello!" | Normal greeting response |
| "I'm feeling sad" | Detects **sadness** emotion, empathetic response |
| "I'm so happy!" | Detects **joy** emotion, positive response |
| "I want to end my life" | **Crisis detected**, shows helpline info |

---

## 🧪 Run Tests

```bash
# API endpoint tests
python test_api.py

# Interactive testing
python test_api.py interactive

# Full evaluation suite
python evaluate.py

# Interactive demo
python demo_script.py
```

---

## 📁 Project Overview

```
AI-ChatBot/
├── app.py                 # Backend server (FastAPI)
├── crisis_detector.py     # Crisis detection logic
├── train_emotion.py       # Train emotion model
├── fine_tune.py          # Train response model
├── test_api.py           # API tests
├── evaluate.py           # Evaluation suite
├── demo_script.py        # Interactive demo
│
├── frontend/             # React UI
│   ├── src/App.jsx      # Main component
│   └── package.json     # Dependencies
│
├── models/              # Trained models (created after training)
│   ├── emotion_detector/
│   └── response_model/
│
└── docs/
    ├── README.md        # Full documentation
    ├── SETUP_GUIDE.md   # Detailed setup
    ├── QUICKSTART.md    # Quick reference
    └── ARCHITECTURE.md  # Technical details
```

---

## 🎓 Understanding the System

### How It Works

```
1. User types message → Frontend
2. Frontend sends to Backend API
3. Backend checks for crisis keywords
4. If no crisis:
   a. Detect emotion (BERT model)
   b. Retrieve conversation history
   c. Generate response (DialoGPT model)
   d. Save to memory
5. Return response with emotion label
6. Frontend displays with emotion indicator
```

### Key Components

**Emotion Detection:**
- Model: BERT (fine-tuned on emotion dataset)
- Output: anger, fear, joy, love, sadness, surprise
- Accuracy: ~88-92%

**Response Generation:**
- Model: DialoGPT (fine-tuned on empathetic dialogues)
- Input: Emotion + Context + User message
- Output: Empathetic response

**Crisis Detection:**
- Method: Keyword matching + pattern recognition
- Levels: Low, Medium, High, Critical
- Action: Provide helpline information

**Memory:**
- Stores last 3-5 conversation turns
- Enables context-aware responses

---

## 🎨 Customization

### Change Crisis Region

Edit `app.py` line 67:

```python
crisis_detector = get_detector(region="us")  # or "uk", "international"
```

### Modify Emotions

Edit `app.py` TONE_GUIDELINES (lines 40-48):

```python
TONE_GUIDELINES = {
    "sadness": "Your custom instruction here",
    # ...
}
```

### Update UI Colors

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  primary: {
    500: '#your-color-here'
  }
}
```

---

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" error:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Port 8000 already in use":**
```bash
# Use different port
uvicorn app:app --port 8001
```

**"CUDA out of memory" during training:**
```bash
# Reduce batch size in train_emotion.py:
per_device_train_batch_size=8  # Change from 16
```

### Frontend Issues

**"npm install" fails:**
```bash
# Clear cache and retry
npm cache clean --force
npm install
```

**Blank page in browser:**
- Check browser console for errors
- Verify backend is running
- Check proxy settings in vite.config.js

**"Failed to fetch" errors:**
- Ensure backend is running on port 8000
- Check CORS settings in app.py
- Verify proxy configuration

### Model Issues

**Models not downloading:**
- Check internet connection
- Verify you have enough disk space (10GB+)
- Try running with `--no-cache-dir` flag

**Low accuracy after training:**
- Train for more epochs (edit training scripts)
- Use larger batch size if you have more RAM
- Ensure dataset downloaded correctly

---

## 📚 Next Steps

### For Learning

1. **Understand the Code**
   - Read `app.py` to see API logic
   - Check `crisis_detector.py` for safety features
   - Explore `frontend/src/App.jsx` for UI

2. **Experiment**
   - Modify tone guidelines
   - Add new emotions
   - Change UI styling
   - Add new features

3. **Evaluate**
   - Run `python evaluate.py`
   - Test with different messages
   - Measure response quality

### For PBL Project

1. **Documentation**
   - ✅ Architecture diagram (see ARCHITECTURE.md)
   - ✅ Methodology (see README.md)
   - ✅ Evaluation metrics (see evaluate.py)
   - ⏳ Create demo video (2-3 minutes)

2. **Testing**
   - Run all test scripts
   - Document results
   - Create test report

3. **Presentation**
   - Use demo_script.py for live demo
   - Show emotion detection
   - Demonstrate crisis handling
   - Explain architecture

---

## 🆘 Getting Help

### Documentation

- **Full Guide:** [README.md](README.md)
- **Setup Details:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Quick Reference:** [QUICKSTART.md](QUICKSTART.md)

### Common Questions

**Q: Do I need a GPU?**  
A: No, but training is much faster with GPU (30 min vs 2 hours).

**Q: Can I skip training?**  
A: Yes! The system works with base models, just less optimized.

**Q: Is this production-ready?**  
A: For educational purposes, yes. For real users, add authentication, persistent storage, and professional review.

**Q: Can I deploy this online?**  
A: Yes! See deployment section in README.md.

---

## 🎯 Success Checklist

Before your PBL presentation, ensure:

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Can send and receive messages
- [ ] Emotion detection works (test all 6 emotions)
- [ ] Crisis detection triggers (test with crisis message)
- [ ] Conversation memory works (ask bot to remember)
- [ ] Tests pass (`python test_api.py`)
- [ ] Evaluation runs (`python evaluate.py`)
- [ ] Demo script works (`python demo_script.py`)
- [ ] Documentation is complete
- [ ] Demo video created (optional but recommended)

---

## 🌟 Tips for Success

1. **Start Simple:** Use base models first, train later
2. **Test Early:** Run tests frequently to catch issues
3. **Read Errors:** Error messages usually tell you what's wrong
4. **Ask for Help:** Check documentation or create GitHub issue
5. **Document Everything:** Keep notes of what you learn
6. **Practice Demo:** Run through demo_script.py multiple times

---

## 📞 Emergency Resources

**If you encounter crisis messages while testing:**

Remember, this is an AI tool for education. Real crisis situations require professional help:

- **India:** AASRA - 91-9820466726
- **USA:** 988 Suicide & Crisis Lifeline
- **UK:** Samaritans - 116 123
- **International:** [IASP Resources](https://www.iasp.info/resources/Crisis_Centres/)

---

## 🎉 You're Ready!

You now have everything you need to run MindMate. Start with Option 1 (Quick Start) to see it in action, then move to Option 2 for the full experience.

**Good luck with your PBL project! 🧠❤️**

---

*For detailed information, see [README.md](README.md) | For quick reference, see [QUICKSTART.md](QUICKSTART.md)*
