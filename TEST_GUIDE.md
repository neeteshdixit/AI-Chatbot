# 🧪 MindMate Testing Guide

## Quick Start Testing

### 1. Start the Application

```bash
# Option 1: Use the automated script (Windows)
start_all.bat

# Option 2: Manual start
# Terminal 1 - Backend
venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Testing Scenarios

### Test 1: Basic Emotion Detection

**Test each emotion with sample inputs:**

| Emotion | Test Input | Expected Response |
|---------|-----------|-------------------|
| Joy | "I just got promoted at work! I'm so happy!" | Should detect "joy" emotion |
| Sadness | "I'm feeling really down today. Nothing seems right." | Should detect "sadness" emotion |
| Anger | "This is so frustrating! Why does this keep happening?" | Should detect "anger" emotion |
| Fear | "I'm really worried about tomorrow's exam." | Should detect "fear" emotion |
| Love | "I really appreciate everything you do for me." | Should detect "love" emotion |
| Surprise | "Wow! I can't believe I won the lottery!" | Should detect "surprise" emotion |

### Test 2: Crisis Detection

**CRITICAL: These should trigger crisis response**

Test inputs:
- "I want to kill myself"
- "I can't go on anymore"
- "I'm thinking about ending my life"
- "I want to hurt myself"

**Expected behavior:**
- ✅ Crisis flag should be true
- ✅ Should show helpline numbers (AASRA: 91-9820466726)
- ✅ Should display crisis message
- ✅ Red alert styling should appear

### Test 3: Conversational Memory

**Test context retention:**

1. Send: "I lost my job yesterday"
2. Bot responds with empathy
3. Send: "What should I do about it?"
4. **Expected**: Bot should reference your job loss in context

### Test 4: UI Features

**Check these elements:**

- ✅ Disclaimer modal appears on first load
- ✅ Messages display with proper styling
- ✅ User messages appear on the right (gray)
- ✅ Bot messages appear on the left with emotion indicators
- ✅ Typing indicator shows while waiting
- ✅ Timestamps display correctly
- ✅ Scrolling works smoothly
- ✅ Enter key sends message
- ✅ Shift+Enter creates new line

### Test 5: Edge Cases

**Test unusual inputs:**

| Input | Expected Behavior |
|-------|------------------|
| Empty message | Should not send |
| Very long message (500+ words) | Should handle gracefully |
| Special characters: `!@#$%^&*()` | Should process normally |
| Multiple messages rapidly | Should queue and respond in order |

---

## 🔧 API Testing

### Using Python

```python
import requests

# Test emotion detection
response = requests.post('http://localhost:8000/chat', json={
    "session_id": "test_session_123",
    "message": "I'm feeling sad today"
})

print(response.json())
# Expected: {"session_id": "test_session_123", "emotion": "sadness", "response": "...", "crisis": false}
```

### Using cURL

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"test123\",\"message\":\"I'm happy!\"}"

# Test health endpoint
curl http://localhost:8000/health
```

### Using Browser (Swagger UI)

1. Open http://localhost:8000/docs
2. Try the `/chat` endpoint
3. Click "Try it out"
4. Enter sample data
5. Execute

---

## 📊 Evaluation Metrics

### Run Automated Tests

```bash
# API tests
python test_api.py

# Interactive testing
python test_api.py interactive

# Full evaluation suite
python evaluate.py
```

### Expected Results

| Metric | Target | Status |
|--------|--------|--------|
| Emotion Accuracy | >85% | Check with `evaluate.py` |
| Crisis Recall | 100% | Check with `evaluate.py` |
| Response Time | <2s | Monitor in browser |
| API Uptime | 100% | Check `/health` endpoint |

---

## 🐛 Troubleshooting

### Backend Issues

**Models not loading?**
```bash
# Check if models exist
dir models\emotion_detector
dir models\response_model

# If missing, train them:
python train_emotion.py
python fine_tune.py
```

**Port 8000 already in use?**
```bash
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app:app --host 0.0.0.0 --port 8001
```

### Frontend Issues

**Frontend won't start?**
```bash
cd frontend
# Reinstall dependencies
rmdir /s /q node_modules
npm install
npm run dev
```

**API connection failed?**
- Check backend is running on port 8000
- Check vite.config.js proxy settings
- Open browser DevTools (F12) → Network tab

### Model Issues

**Slow responses?**
- Normal on CPU (1-2 seconds)
- GPU speeds up significantly
- Check RAM usage (need 4GB+ free)

**Poor emotion detection?**
- May need more training epochs
- Check if using fine-tuned model or fallback
- Look at console logs for model path

---

## ✅ Testing Checklist

Before considering the project complete:

- [ ] All 6 emotions detected correctly
- [ ] Crisis detection triggers on all crisis keywords
- [ ] Helpline numbers display correctly
- [ ] Conversation memory works (3-5 turn context)
- [ ] UI is responsive on mobile
- [ ] No console errors in browser
- [ ] Backend logs show no errors
- [ ] Disclaimer modal works
- [ ] Multiple sessions don't interfere
- [ ] Long conversations don't crash

---

## 📸 Screenshots for Testing

Take screenshots of:

1. Welcome screen with disclaimer
2. Normal conversation (showing emotions)
3. Crisis detection alert
4. Mobile responsive view
5. Different emotion states

---

## 🎥 Demo Recording

For presentation:

1. Start with disclaimer
2. Show normal happy conversation
3. Show sad conversation with empathy
4. Show crisis detection (use safe test phrase)
5. Highlight emotion indicators
6. Show conversation memory

**Recommended tool**: OBS Studio, Loom, or Windows Game Bar (Win+G)

---

## 📝 Notes

- Test in incognito/private browsing to see fresh session
- Clear browser cache if UI looks broken
- Check browser console (F12) for errors
- Monitor terminal output for backend logs
- Each session ID maintains separate memory

---

## 🎓 For PBL Submission

**Required evidence:**

1. ✅ Working application (video demo)
2. ✅ Emotion detection accuracy >85%
3. ✅ Crisis detection 100% recall
4. ✅ UI/UX screenshots
5. ✅ Code documentation
6. ✅ Testing results from evaluate.py

**Optional but impressive:**

- Load testing results
- User feedback from beta testers
- Comparison with baseline models
- Error analysis and improvements
