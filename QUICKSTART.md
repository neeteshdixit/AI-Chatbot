# 🚀 MindMate Quick Start Guide

Get MindMate running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- 8GB RAM

## Installation

### 1. Install Backend Dependencies

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Backend (with base models)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Note:** First run will download base models (~1GB). This may take a few minutes.

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Start Frontend

```bash
npm run dev
```

### 5. Open Browser

Go to: **http://localhost:3000**

## Quick Test

Try these messages:

1. "Hello, how are you?"
2. "I'm feeling sad today"
3. "I'm so happy about my new job!"

## Optional: Train Custom Models

For better performance, train the models:

```bash
# Train emotion detector (~30 min on GPU)
python train_emotion.py

# Train response generator (~1 hour on GPU)
python fine_tune.py
```

## Troubleshooting

**Port already in use?**
```bash
# Change backend port
uvicorn app:app --port 8001

# Change frontend port (edit vite.config.js)
server: { port: 3001 }
```

**Models not loading?**
- Check internet connection (downloads from HuggingFace)
- Ensure 8GB+ RAM available
- Try restarting the server

## Next Steps

- Read [README.md](README.md) for full documentation
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- Run tests: `python test_api.py`
- Try demo: `python demo_script.py`

## Using Startup Scripts

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

---

**Need help?** Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) or open an issue on GitHub.
