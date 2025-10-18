# 🚀 MindMate Setup Guide

Complete step-by-step guide to set up and run MindMate on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **8GB+ RAM** (16GB recommended for training)
- **10GB+ free disk space**
- **GPU (optional)** - Speeds up training significantly

---

## 🔧 Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-ChatBot.git
cd AI-ChatBot
```

---

## 🐍 Step 2: Set Up Python Environment

### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Linux/Mac

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note:** Installation may take 5-10 minutes depending on your internet speed.

---

## 🧠 Step 3: Train the Models

### Option A: Train Both Models (Recommended)

This will give you the best performance but takes time.

#### 3.1 Train Emotion Detection Model

```bash
python train_emotion.py
```

**What happens:**
- Downloads `dair-ai/emotion` dataset (~5MB)
- Fine-tunes BERT model for 3 epochs
- Saves model to `./models/emotion_detector/`

**Time required:**
- GPU: 15-30 minutes
- CPU: 1-2 hours

**Expected output:**
```
Loading dataset...
Labels: ['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']
Loading tokenizer and model...
Tokenizing...
Training...
Epoch 1/3: 100%|████████| 1000/1000 [05:23<00:00]
...
Saved emotion model to ./models/emotion_detector
```

#### 3.2 Train Response Generation Model

```bash
python fine_tune.py
```

**What happens:**
- Downloads `empathetic_dialogues` dataset (~50MB)
- Fine-tunes DialoGPT model for 3 epochs
- Saves model to `./models/response_model/`

**Time required:**
- GPU: 30-60 minutes
- CPU: 2-4 hours

**Expected output:**
```
Loading empathetic_dialogues...
Converting to prompts...
Loading tokenizer & model...
Tokenizing...
Starting training...
Epoch 1/3: 100%|████████| 5000/5000 [15:42<00:00]
...
Saved response model to ./models/response_model
```

### Option B: Use Pre-trained Models (Quick Start)

If you want to test the system quickly without training:

```bash
# The app will automatically use base models if fine-tuned models aren't found
# Emotion: bert-base-uncased
# Response: microsoft/DialoGPT-small
```

**Note:** Pre-trained models will work but won't be optimized for mental health conversations.

---

## 🚀 Step 4: Start the Backend Server

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Start FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Expected output:**
```
Loading emotion model: ./models/emotion_detector
Loading response model: ./models/response_model
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Test the API:**

Open a new terminal and run:
```bash
curl http://localhost:8000/health
```

Expected response: `{"status":"ok"}`

---

## 💻 Step 5: Set Up the Frontend

Open a **new terminal** (keep the backend running):

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

**Note:** This may take 2-5 minutes.

**Start the development server:**

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

---

## 🎉 Step 6: Access the Application

1. **Open your browser** and go to: `http://localhost:3000`

2. **You should see:**
   - A disclaimer modal (click "I Understand, Continue")
   - The MindMate chat interface
   - A welcome message from the bot

3. **Try these test messages:**
   - "Hello, how are you?"
   - "I'm feeling sad today"
   - "I'm so happy about my new job!"
   - "I feel worthless and hopeless" (will trigger crisis detection)

---

## ✅ Step 7: Verify Everything Works

### Test Emotion Detection

Send these messages and check if emotions are detected correctly:

| Message | Expected Emotion |
|---------|-----------------|
| "I'm so happy!" | joy |
| "I feel sad and lonely" | sadness |
| "This makes me so angry!" | anger |
| "I'm scared about the future" | fear |
| "I love spending time with you" | love |
| "Wow, I can't believe it!" | surprise |

### Test Crisis Detection

Send: "I want to end my life"

**Expected behavior:**
- Emotion shows as "crisis"
- Red alert styling
- Response includes helpline numbers (AASRA: 91-9820466726)

### Test Memory

1. Send: "My name is Alex"
2. Send: "I'm feeling stressed"
3. Send: "Do you remember my name?"

**Expected:** Bot should reference earlier context.

---

## 🧪 Step 8: Run Tests (Optional)

### API Tests

```bash
# Automated test suite
python test_api.py

# Interactive testing
python test_api.py interactive
```

### Full Evaluation

```bash
python evaluate.py
```

This will:
- Evaluate emotion model accuracy
- Test crisis detection recall
- Provide manual evaluation guidelines

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "CUDA out of memory" during training

**Solution:**
```bash
# Reduce batch size in training scripts
# Edit train_emotion.py line 53:
per_device_train_batch_size=8  # Change from 16 to 8

# Edit fine_tune.py line 75:
per_device_train_batch_size=2  # Change from 4 to 2
```

### Issue: Frontend shows "Failed to fetch"

**Solution:**
1. Check if backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in `app.py` (lines 54-60)
3. Make sure both servers are running

### Issue: Models take too long to train

**Solution:**
- Use fewer epochs (change `num_train_epochs=1` in training scripts)
- Use smaller dataset subset
- Or skip training and use base models

### Issue: Port already in use

**Solution:**
```bash
# Backend (change port)
uvicorn app:app --host 0.0.0.0 --port 8001

# Frontend (edit vite.config.js)
server: { port: 3001 }
```

---

## 🔄 Daily Development Workflow

### Starting the Application

```bash
# Terminal 1: Backend
cd AI-ChatBot
venv\Scripts\activate  # or source venv/bin/activate
uvicorn app:app --reload  # --reload for auto-restart on changes

# Terminal 2: Frontend
cd AI-ChatBot/frontend
npm run dev
```

### Stopping the Application

- Press `Ctrl+C` in both terminals
- Or close the terminal windows

---

## 📊 Performance Optimization

### For Faster Inference

1. **Use GPU if available:**
   - PyTorch will automatically use CUDA if available
   - Check with: `python -c "import torch; print(torch.cuda.is_available())"`

2. **Reduce model size:**
   - Use `DialoGPT-small` instead of `medium` or `large`
   - Use `distilbert-base-uncased` instead of `bert-base-uncased`

3. **Enable model quantization:**
   ```python
   # In app.py, after loading models:
   model = torch.quantization.quantize_dynamic(
       model, {torch.nn.Linear}, dtype=torch.qint8
   )
   ```

---

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Note:** You still need to train models first or mount pre-trained models.

---

## 📚 Next Steps

1. **Customize the chatbot:**
   - Edit tone guidelines in `app.py`
   - Modify crisis keywords in `crisis_detector.py`
   - Change UI colors in `frontend/tailwind.config.js`

2. **Improve models:**
   - Train for more epochs
   - Use larger base models
   - Fine-tune on domain-specific data

3. **Add features:**
   - Implement user authentication
   - Add persistent storage (Redis/PostgreSQL)
   - Create admin dashboard

4. **Deploy to production:**
   - Use Render, Railway, or AWS
   - Set up proper logging and monitoring
   - Implement rate limiting and security

---

## 🆘 Getting Help

- **Documentation:** See [README.md](README.md)
- **Issues:** Check existing issues or create a new one
- **Community:** Join discussions on GitHub

---

## ✅ Setup Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Emotion model trained or using base model
- [ ] Response model trained or using base model
- [ ] Backend server running on port 8000
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Disclaimer modal appears
- [ ] Can send messages and receive responses
- [ ] Emotions are detected correctly
- [ ] Crisis detection works
- [ ] Tests pass (`python test_api.py`)

---

**Congratulations! 🎉 MindMate is now running on your machine!**

If you encounter any issues not covered here, please check the [README.md](README.md) or open an issue on GitHub.
