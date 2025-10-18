# ❓ Frequently Asked Questions (FAQ)

Common questions about MindMate chatbot.

---

## General Questions

### What is MindMate?

MindMate is an AI-powered mental health support chatbot that uses emotion detection and empathetic response generation to provide supportive conversations. It's designed as an educational project demonstrating NLP and deep learning in mental health applications.

### Is MindMate a replacement for therapy?

**No.** MindMate is NOT a substitute for professional mental health care. It's an educational tool and support companion. Always seek professional help for serious mental health concerns.

### Is my conversation data stored?

In the current implementation, conversations are stored in memory only and are lost when the server restarts. No data is persisted to disk or sent to external services (except model downloads from HuggingFace).

### Is MindMate free to use?

Yes, the code is open-source under MIT License. You can use, modify, and deploy it freely.

---

## Technical Questions

### Do I need a GPU to run MindMate?

**No, but it helps.** 
- **Without GPU:** Works fine, but model training takes 2-4 hours
- **With GPU:** Training takes 30-60 minutes
- **Inference:** Both work well, GPU is slightly faster

### What are the system requirements?

**Minimum:**
- Python 3.10+
- Node.js 18+
- 4GB RAM
- 5GB disk space

**Recommended:**
- Python 3.10+
- Node.js 18+
- 8GB+ RAM
- 10GB disk space
- GPU (optional)

### Can I use this without training the models?

**Yes!** The system automatically uses pre-trained base models if fine-tuned models aren't found. Performance will be good but not optimized for mental health conversations.

### How long does training take?

**Emotion Model:**
- GPU: 15-30 minutes
- CPU: 1-2 hours

**Response Model:**
- GPU: 30-60 minutes
- CPU: 2-4 hours

### What languages are supported?

Currently **English only**. The models are trained on English datasets. Multi-language support is planned for future versions.

---

## Usage Questions

### How do I start the chatbot?

**Quick method:**
```bash
# Backend
uvicorn app:app --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd frontend
npm run dev
```

**Or use startup scripts:**
- Windows: `start.bat`
- Linux/Mac: `./start.sh`

### The models are downloading slowly. Is this normal?

Yes, first run downloads ~1GB of models from HuggingFace. This can take 5-15 minutes depending on your internet speed. Subsequent runs will be instant.

### Can I change the helpline numbers?

**Yes!** Edit `crisis_detector.py` and update the `HELPLINES` dictionary with your region's helpline information.

### How do I test if it's working correctly?

Run the test suite:
```bash
python test_api.py              # API tests
python evaluate.py              # Full evaluation
python demo_script.py           # Interactive demo
```

---

## Troubleshooting

### "Module not found" error

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### "Port already in use" error

**Solution:**
```bash
# Use different port
uvicorn app:app --port 8001

# Or kill existing process
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### Frontend shows "Failed to fetch"

**Checklist:**
1. Is backend running? Check `http://localhost:8000/health`
2. Check CORS settings in `app.py`
3. Verify proxy settings in `frontend/vite.config.js`
4. Check browser console for errors

### "CUDA out of memory" during training

**Solutions:**
1. Reduce batch size in training scripts
2. Use CPU instead: `export CUDA_VISIBLE_DEVICES=""`
3. Close other applications
4. Use smaller model variant

### Models not loading

**Solutions:**
1. Check internet connection
2. Verify disk space (need 5GB+)
3. Check model paths in `app.py`
4. Try deleting and re-downloading models

### Response quality is poor

**Possible causes:**
1. Using base models instead of fine-tuned
2. Need more training epochs
3. Dataset not downloaded correctly
4. Model not loaded properly

**Solution:** Train models with `python train_emotion.py` and `python fine_tune.py`

---

## Feature Questions

### Can I add more emotions?

**Yes!** You'll need to:
1. Find a dataset with your desired emotions
2. Update `EMOTION_LABELS` in `app.py`
3. Retrain the emotion model
4. Update UI emotion colors

### Can I customize the responses?

**Yes!** Edit `TONE_GUIDELINES` in `app.py` to change how the bot responds to different emotions.

### Can I add voice input/output?

Not currently implemented, but you can add:
- **Input:** Web Speech API for voice-to-text
- **Output:** Text-to-speech libraries

This is a planned future enhancement.

### Can I deploy this to production?

**Yes, but with caution:**
1. Add proper authentication
2. Implement persistent storage
3. Set up monitoring and logging
4. Get professional mental health review
5. Add proper disclaimers and legal terms
6. Ensure GDPR/HIPAA compliance if needed

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

### Can I integrate this with WhatsApp/Telegram?

**Yes!** You can create a bot wrapper:
- **WhatsApp:** Use Twilio API
- **Telegram:** Use python-telegram-bot
- **Discord:** Use discord.py

The FastAPI backend can be called from any platform.

---

## Development Questions

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- Bug fixes
- New features
- Documentation improvements
- Translations
- Testing

### What's the tech stack?

**Backend:**
- FastAPI (API framework)
- PyTorch (deep learning)
- Transformers (NLP models)
- BERT (emotion detection)
- DialoGPT (response generation)

**Frontend:**
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- Axios (HTTP client)

### Can I use a different model?

**Yes!** You can swap models:

**For emotion detection:**
```python
# In train_emotion.py, change:
MODEL_NAME = "distilbert-base-uncased"  # Smaller, faster
# or
MODEL_NAME = "roberta-base"  # Better accuracy
```

**For response generation:**
```python
# In fine_tune.py, change:
MODEL_NAME = "microsoft/DialoGPT-medium"  # Better quality
# or
MODEL_NAME = "facebook/blenderbot-400M-distill"  # Different approach
```

### How do I add a database?

See example implementation:

```python
# Install: pip install sqlalchemy psycopg2-binary

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    session_id = Column(String)
    role = Column(String)
    content = Column(Text)
    emotion = Column(String)

engine = create_engine('postgresql://user:pass@localhost/mindmate')
Base.metadata.create_all(engine)
```

### How do I add user authentication?

Use FastAPI's security features:

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/chat")
async def chat(
    req: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify token
    token = credentials.credentials
    # ... authentication logic
```

---

## Performance Questions

### How fast is the response time?

**Typical response time:**
- Emotion detection: 50-100ms
- Crisis detection: <10ms
- Response generation: 500-1000ms
- **Total:** 600-1200ms

### How many users can it handle?

**Single instance:**
- 10-50 concurrent users (CPU)
- 50-100 concurrent users (GPU)

**With scaling:**
- Unlimited (with load balancer + multiple instances)

### How can I make it faster?

1. **Use GPU** for inference
2. **Quantize models** (INT8)
3. **Cache responses** for common queries
4. **Batch requests** if possible
5. **Use smaller models** (distilbert, DialoGPT-small)

---

## Safety & Ethics Questions

### How accurate is crisis detection?

Our tests show **100% recall** on test cases (no missed crisis messages). However, real-world scenarios are complex. The system uses multiple layers:
- Critical keywords
- Pattern matching
- Severity classification

### What happens when crisis is detected?

The system:
1. Immediately stops normal response generation
2. Provides helpline information (AASRA: 91-9820466726)
3. Encourages immediate professional help
4. Saves the interaction for review

### Can the bot give harmful advice?

The system is designed to:
- Never give medical advice
- Always encourage professional help
- Provide supportive, not prescriptive responses
- Include safety disclaimers

However, AI is not perfect. Always review outputs and have professional oversight for production use.

### Is the bot biased?

Like all AI models, there may be biases from training data. We're working on:
- Diverse dataset inclusion
- Bias detection and mitigation
- Cultural sensitivity improvements
- Regular audits

---

## Licensing & Legal

### Can I use this commercially?

**Yes**, under MIT License. But you must:
- Include the original license
- Add proper disclaimers
- Ensure professional mental health oversight
- Comply with local regulations

### Do I need to credit the project?

Not required by license, but appreciated! You can cite:

```
MindMate - AI Mental Health Chatbot
https://github.com/yourusername/AI-ChatBot
```

### What about HIPAA/GDPR compliance?

The current implementation is NOT compliant. For production:
- Implement proper data encryption
- Add consent mechanisms
- Create privacy policy
- Implement data deletion
- Consult legal experts

---

## Future Plans

### What features are planned?

**Short-term:**
- Multi-language support
- Voice interaction
- Mobile app
- Better analytics

**Long-term:**
- GPT-4 integration
- Personalization
- Therapist dashboard
- Integration with real helplines

### When will X feature be added?

This is an open-source project. Features are added based on:
- Community contributions
- Maintainer availability
- User feedback

Want a feature? Consider contributing!

---

## Getting Help

### Where can I get support?

1. **Documentation:** Check README.md and guides
2. **Issues:** Search existing GitHub issues
3. **Discussions:** Ask in GitHub Discussions
4. **Email:** Contact maintainers

### How do I report a bug?

1. Check if already reported
2. Create GitHub issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Error logs

### How do I request a feature?

Create a GitHub issue with:
- Use case description
- Expected behavior
- Why it's valuable
- Potential implementation approach

---

## Still Have Questions?

- 📖 Read the [README.md](README.md)
- 🔧 Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🏗️ See [ARCHITECTURE.md](ARCHITECTURE.md)
- 🚀 Review [DEPLOYMENT.md](DEPLOYMENT.md)
- 💬 Ask in GitHub Discussions

---

**Last Updated:** 2024  
**Version:** 1.0.0
