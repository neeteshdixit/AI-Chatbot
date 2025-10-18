# 🏗️ MindMate System Architecture

Detailed technical architecture documentation for the MindMate mental health chatbot system.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Model Architecture](#model-architecture)
5. [API Design](#api-design)
6. [Database Schema](#database-schema)
7. [Security & Privacy](#security--privacy)
8. [Scalability Considerations](#scalability-considerations)

---

## System Overview

MindMate is a **three-tier architecture** mental health chatbot system:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                   (React Frontend)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (HTTP/JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                   Application Layer                          │
│                   (FastAPI Backend)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Session    │  │   Request    │  │   Response   │      │
│  │  Management  │  │   Routing    │  │  Formation   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Service Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Emotion    │  │   Response   │  │    Crisis    │      │
│  │  Detection   │  │  Generation  │  │  Detection   │      │
│  │   Service    │  │   Service    │  │   Service    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  In-Memory   │  │    Model     │  │   Training   │      │
│  │   Storage    │  │   Storage    │  │     Data     │      │
│  │  (Sessions)  │  │  (Weights)   │  │  (Datasets)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Frontend (React + Vite + TailwindCSS)

**Purpose:** User interface for chatbot interaction

**Key Components:**

```
frontend/
├── src/
│   ├── App.jsx                 # Main application component
│   │   ├── DisclaimerModal     # Safety disclaimer
│   │   ├── Header              # App header with branding
│   │   ├── ChatContainer       # Message display area
│   │   └── InputArea           # Message input interface
│   │
│   ├── main.jsx                # React entry point
│   ├── index.css               # Global styles + Tailwind
│   └── App.css                 # Component-specific styles
│
├── vite.config.js              # Vite configuration + proxy
├── tailwind.config.js          # TailwindCSS theme
└── package.json                # Dependencies
```

**Key Features:**
- Real-time message rendering
- Emotion visualization (emojis + color coding)
- Crisis alert styling
- Responsive design (mobile-first)
- Accessibility (ARIA labels, keyboard navigation)

**State Management:**
```javascript
// Local state (useState)
- messages: Array<Message>        // Chat history
- inputText: string               // Current input
- isLoading: boolean              // API call status
- sessionId: string               // Unique session identifier
- showDisclaimer: boolean         // Disclaimer modal visibility
```

**API Communication:**
```javascript
// Axios POST to /chat endpoint
axios.post('/chat', {
  session_id: sessionId,
  message: inputText
})
```

---

### 2. Backend (FastAPI)

**Purpose:** API server, request routing, business logic

**File:** `app.py`

**Key Endpoints:**

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/chat` | POST | Send message, get response | `{session_id, message}` | `{session_id, emotion, response, crisis}` |
| `/health` | GET | Health check | None | `{status: "ok"}` |

**Core Functions:**

```python
# Model Loading
load_emotion_model()          # Load BERT classifier
load_response_model()         # Load DialoGPT generator

# Processing Pipeline
detect_crisis(text)           # Check for crisis keywords/patterns
detect_emotion(text)          # Classify emotion (6 classes)
get_context(session_id)       # Retrieve conversation history
generate_response_with_tone() # Generate empathetic response
add_memory()                  # Store conversation turn
```

**Middleware:**
- CORS (Cross-Origin Resource Sharing)
- Request validation (Pydantic)
- Error handling

---

### 3. Emotion Detection Service

**Purpose:** Classify user message into one of 6 emotions

**Model:** Fine-tuned `bert-base-uncased`

**Architecture:**
```
Input Text
    ↓
Tokenizer (WordPiece)
    ↓
BERT Encoder (12 layers, 768 hidden)
    ↓
Classification Head (Linear layer)
    ↓
Softmax
    ↓
Emotion Label: [anger, fear, joy, love, sadness, surprise]
```

**Training Details:**
- Dataset: `dair-ai/emotion` (20k samples)
- Optimizer: AdamW
- Learning rate: 2e-5
- Batch size: 16
- Epochs: 3
- Loss: Cross-entropy

**Inference:**
```python
inputs = tokenizer(text, return_tensors="pt", truncation=True)
logits = model(**inputs).logits
emotion_id = torch.argmax(logits, dim=-1)
emotion = EMOTION_LABELS[emotion_id]
```

**Performance:**
- Accuracy: ~88-92%
- Inference time: 50-100ms
- Memory: ~500MB (model weights)

---

### 4. Response Generation Service

**Purpose:** Generate empathetic, context-aware responses

**Model:** Fine-tuned `microsoft/DialoGPT-small`

**Architecture:**
```
Prompt Construction:
    Tone Instruction + Emotion + Context + User Message
    ↓
Tokenizer
    ↓
DialoGPT Transformer (12 layers, 768 hidden)
    ↓
Autoregressive Generation (top-p sampling)
    ↓
Generated Response
```

**Prompt Template:**
```
{tone_instruction}
Emotion: {emotion}
Context: {last_3_5_messages}
User: {user_message}
Bot:
```

**Training Details:**
- Dataset: `empathetic_dialogues` (25k conversations)
- Optimizer: AdamW
- Learning rate: 5e-5
- Batch size: 4
- Epochs: 3
- Loss: Causal language modeling

**Generation Parameters:**
```python
max_length = input_length + 120
do_sample = True
top_p = 0.9
top_k = 40
temperature = 0.8
```

**Performance:**
- Generation time: 500-1000ms
- Memory: ~350MB (model weights)
- BLEU score: ~0.15-0.25

---

### 5. Crisis Detection Service

**Purpose:** Identify crisis situations with 100% recall priority

**File:** `crisis_detector.py`

**Multi-Layer Detection:**

```
Input Text
    ↓
┌─────────────────────────────────────┐
│ Layer 1: Critical Keywords          │
│ - "suicide", "kill myself", etc.    │
│ → CRITICAL level                    │
└─────────────────────────────────────┘
    ↓ (if not detected)
┌─────────────────────────────────────┐
│ Layer 2: Pattern Matching           │
│ - Regex patterns for indirect expr. │
│ → HIGH level                        │
└─────────────────────────────────────┘
    ↓ (if not detected)
┌─────────────────────────────────────┐
│ Layer 3: Concerning Keywords        │
│ - "worthless", "hopeless", etc.     │
│ → MEDIUM/LOW level                  │
└─────────────────────────────────────┘
    ↓
Crisis Level: [NONE, LOW, MEDIUM, HIGH, CRITICAL]
```

**Crisis Levels:**

| Level | Description | Response |
|-------|-------------|----------|
| CRITICAL | Direct suicidal intent | Immediate helpline + emergency services |
| HIGH | Indirect suicidal ideation | Helpline + strong encouragement to seek help |
| MEDIUM | Multiple concerning signals | Helpline + supportive message |
| LOW | Single concerning keyword | Gentle check-in + helpline mention |
| NONE | No crisis indicators | Normal conversation |

**Helpline Database:**
```python
HELPLINES = {
    "india": {"name": "AASRA", "number": "91-9820466726"},
    "us": {"name": "988 Lifeline", "number": "988"},
    "uk": {"name": "Samaritans", "number": "116 123"},
    "international": {"url": "iasp.info/resources/Crisis_Centres/"}
}
```

---

### 6. Memory Management

**Purpose:** Maintain conversation context

**Implementation:** In-memory dictionary

```python
CONVERSATION_MEMORY = {
    "session_id_1": [
        {"user": "I'm feeling sad", "bot": "I'm sorry to hear that..."},
        {"user": "I can't sleep", "bot": "Sleep issues can be tough..."},
        # ... up to MAX_MEMORY (5) exchanges
    ],
    "session_id_2": [...]
}
```

**Operations:**

```python
# Add to memory
def add_memory(session_id, user_text, bot_text):
    lst = CONVERSATION_MEMORY.setdefault(session_id, [])
    lst.append({"user": user_text, "bot": bot_text})
    if len(lst) > MAX_MEMORY:
        CONVERSATION_MEMORY[session_id] = lst[-MAX_MEMORY:]

# Retrieve context
def get_context(session_id):
    items = CONVERSATION_MEMORY.get(session_id, [])
    return "\n".join([f"User: {e['user']}\nBot: {e['bot']}" 
                      for e in items[-MAX_MEMORY:]])
```

**Limitations:**
- Not persistent (lost on server restart)
- No cross-session memory
- Limited to 5 turns

**Future Enhancement:**
- Redis for persistent storage
- PostgreSQL for long-term history
- User profiles with preferences

---

## Data Flow

### Complete Request-Response Cycle

```
1. User types message in frontend
   ↓
2. Frontend sends POST /chat with {session_id, message}
   ↓
3. Backend receives request
   ↓
4. Crisis Detection (parallel check)
   ├─ If crisis detected → Return crisis message immediately
   └─ If no crisis → Continue
   ↓
5. Emotion Detection
   ├─ Tokenize input
   ├─ BERT inference
   └─ Get emotion label
   ↓
6. Memory Retrieval
   └─ Fetch last 3-5 conversation turns
   ↓
7. Response Generation
   ├─ Build prompt (tone + emotion + context + message)
   ├─ DialoGPT inference
   └─ Decode generated tokens
   ↓
8. Memory Update
   └─ Store user message + bot response
   ↓
9. Return response {session_id, emotion, response, crisis}
   ↓
10. Frontend displays message with emotion indicator
```

**Timing Breakdown:**
- Request validation: <5ms
- Crisis detection: <10ms
- Emotion detection: 50-100ms
- Context retrieval: <5ms
- Response generation: 500-1000ms
- Memory update: <5ms
- **Total: ~600-1200ms**

---

## Model Architecture

### BERT Emotion Classifier

```
Input: "I'm feeling sad today"
    ↓
Tokenizer: [CLS] i'm feeling sad today [SEP]
    ↓
Token IDs: [101, 1045, 1005, 1049, 3110, 6517, 2651, 102]
    ↓
Embedding Layer (768-dim)
    ↓
12 × Transformer Encoder Blocks
    ├─ Multi-Head Self-Attention (12 heads)
    ├─ Layer Normalization
    ├─ Feed-Forward Network
    └─ Residual Connections
    ↓
[CLS] Token Representation (768-dim)
    ↓
Dropout (0.1)
    ↓
Linear Layer (768 → 6)
    ↓
Softmax
    ↓
Output: [0.05, 0.08, 0.12, 0.10, 0.62, 0.03]
         anger  fear   joy   love  sadness surprise
    ↓
Predicted: sadness (0.62 confidence)
```

### DialoGPT Response Generator

```
Input Prompt:
"Respond softly, with empathy and concrete small-step suggestions.
Emotion: sadness
Context: [previous conversation]
User: I'm feeling sad today
Bot:"
    ↓
Tokenizer: Convert to token IDs
    ↓
12 × Transformer Decoder Blocks
    ├─ Masked Multi-Head Self-Attention
    ├─ Layer Normalization
    ├─ Feed-Forward Network
    └─ Residual Connections
    ↓
Autoregressive Generation (token by token)
    ├─ Sample from top-p (0.9) distribution
    ├─ Temperature scaling (0.8)
    └─ Stop at [EOS] or max_length
    ↓
Generated Tokens: [1045, 1005, 1049, 2061, 3374, ...]
    ↓
Decode to Text:
"I'm so sorry you're feeling sad. Would you like to talk about 
what's been troubling you? Sometimes sharing can help lighten 
the burden."
```

---

## API Design

### Request Schema

```json
{
  "session_id": "string (required)",
  "message": "string (required, non-empty)"
}
```

### Response Schema

```json
{
  "session_id": "string",
  "emotion": "string (anger|fear|joy|love|sadness|surprise|crisis|neutral)",
  "response": "string",
  "crisis": "boolean"
}
```

### Error Responses

```json
// 400 Bad Request
{
  "detail": "Empty message"
}

// 500 Internal Server Error
{
  "detail": "Model inference failed"
}
```

### Rate Limiting (Future)

```
- 60 requests per minute per IP
- 1000 requests per hour per session
- Exponential backoff on repeated failures
```

---

## Database Schema

### Current: In-Memory Storage

```python
# Session-based conversation memory
{
  "session_abc123": [
    {"user": "...", "bot": "...", "timestamp": "..."},
    ...
  ]
}
```

### Future: PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP,
    preferences JSONB
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    metadata JSONB
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    role VARCHAR(10) CHECK (role IN ('user', 'bot')),
    content TEXT NOT NULL,
    emotion VARCHAR(20),
    crisis_detected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_session_created (session_id, created_at)
);

-- Crisis events table (for monitoring)
CREATE TABLE crisis_events (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    message_id UUID REFERENCES messages(id),
    severity VARCHAR(20),
    detected_at TIMESTAMP DEFAULT NOW(),
    keywords TEXT[],
    action_taken TEXT
);
```

---

## Security & Privacy

### Current Implementation

1. **No Persistent Storage**
   - Conversations stored in memory only
   - Lost on server restart
   - No long-term data retention

2. **No Authentication**
   - Anonymous sessions
   - Session ID generated client-side

3. **CORS Protection**
   - Limited to localhost origins
   - Prevents unauthorized cross-origin requests

### Production Requirements

1. **Data Encryption**
   - HTTPS/TLS for all communications
   - Encrypt sensitive data at rest
   - Secure session tokens (JWT)

2. **Privacy Compliance**
   - GDPR compliance (EU)
   - HIPAA compliance (US healthcare)
   - Data anonymization
   - Right to deletion

3. **Access Control**
   - User authentication (OAuth 2.0)
   - Role-based access control
   - API key management

4. **Audit Logging**
   - Log all crisis detections
   - Track model predictions
   - Monitor for abuse

5. **Content Filtering**
   - Prevent prompt injection
   - Filter inappropriate content
   - Rate limiting

---

## Scalability Considerations

### Current Limitations

- Single server instance
- In-memory storage (not scalable)
- Synchronous request handling
- No load balancing

### Scaling Strategy

#### Horizontal Scaling

```
                    ┌─────────────┐
                    │ Load        │
Internet ──────────>│ Balancer    │
                    │ (Nginx)     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼────┐      ┌─────▼────┐
   │ FastAPI │       │ FastAPI  │      │ FastAPI  │
   │ Server 1│       │ Server 2 │      │ Server 3 │
   └────┬────┘       └─────┬────┘      └─────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Redis     │
                    │  (Sessions) │
                    └─────────────┘
```

#### Model Serving Optimization

1. **Model Quantization**
   - INT8 quantization (4x smaller, 2-4x faster)
   - Minimal accuracy loss (<1%)

2. **Model Caching**
   - Keep models in GPU memory
   - Batch inference for multiple requests

3. **Separate Model Servers**
   - Dedicated servers for emotion detection
   - Dedicated servers for response generation
   - gRPC communication

4. **CDN for Static Assets**
   - Frontend served via CDN
   - Reduced latency globally

#### Database Optimization

1. **Connection Pooling**
   - Reuse database connections
   - Reduce connection overhead

2. **Caching Layer**
   - Redis for session data
   - Memcached for frequent queries

3. **Read Replicas**
   - Separate read/write databases
   - Distribute query load

---

## Monitoring & Observability

### Metrics to Track

1. **Performance Metrics**
   - Request latency (p50, p95, p99)
   - Throughput (requests/second)
   - Error rate

2. **Model Metrics**
   - Emotion detection accuracy
   - Crisis detection recall
   - Response generation time

3. **Business Metrics**
   - Active sessions
   - Messages per session
   - Crisis events per day

### Logging Strategy

```python
import logging

logger = logging.getLogger("mindmate")

# Log levels
logger.info("User message received")
logger.warning("High response latency detected")
logger.error("Model inference failed")
logger.critical("Crisis detection system down")
```

### Alerting

- Crisis detection failures → Immediate alert
- High error rate → Alert within 5 minutes
- Server down → Immediate alert

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI framework |
| | Vite | Build tool |
| | TailwindCSS | Styling |
| | Axios | HTTP client |
| Backend | FastAPI | API framework |
| | Uvicorn | ASGI server |
| | Pydantic | Data validation |
| ML/NLP | Transformers | Model library |
| | PyTorch | Deep learning |
| | Datasets | Data loading |
| Storage | In-memory dict | Session storage |
| | (Future) Redis | Cache layer |
| | (Future) PostgreSQL | Persistent storage |
| DevOps | Docker | Containerization |
| | Docker Compose | Orchestration |
| Testing | Pytest | Unit tests |
| | httpx | API testing |

---

## Deployment Architecture

### Development
```
Localhost:3000 (Frontend) → Localhost:8000 (Backend)
```

### Production (Example: AWS)

```
Route 53 (DNS)
    ↓
CloudFront (CDN) → S3 (Frontend static files)
    ↓
ALB (Load Balancer)
    ↓
ECS/Fargate (Backend containers)
    ↓
├─ ElastiCache (Redis)
└─ RDS PostgreSQL
```

---

This architecture is designed to be:
- **Modular:** Easy to replace components
- **Scalable:** Can handle increased load
- **Maintainable:** Clear separation of concerns
- **Secure:** Privacy and safety by design
- **Extensible:** Easy to add new features

For implementation details, see the source code and README.md.
