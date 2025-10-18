 # app.py
"""
FastAPI server that:
- loads emotion classifier and response generator
- keeps per-session short-term memory (last 3-5 exchanges)
- does crisis detection and returns helpline text
- generates emotion-conditioned replies (tone control instructions)
Run:
    uvicorn app:app --host 0.0.0.0 --port 8000
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM
from crisis_detector import get_detector, CrisisLevel

# Model paths - adjust if you saved to different locations
EMOTION_MODEL_DIR = "./models/emotion_detector"   # from train_emotion.py
RESPONSE_MODEL_DIR = "./models/response_model"    # from fine_tune_response.py

# Fallback to pre-trained if local fine-tuned not available
DEFAULT_EMOTION_MODEL = "bert-base-uncased"
DEFAULT_RESPONSE_MODEL = "microsoft/DialoGPT-small"

# Crisis keywords and local helpline (example India numbers)
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die",
    "kill myself", "worthless", "can't go on", "hopeless", "self harm", "self-harm"
]

CRISIS_MESSAGE = (
    "I'm really sorry you're feeling this way. If you're in immediate danger, "
    "please call your local emergency number. If you are in India, you can contact AASRA Helpline at 91-9820466726.\n"
    "Would you like me to provide some resources or connect you to a human right now?"
)

# Tone guidelines
TONE_GUIDELINES = {
    "sadness": "Respond softly, with empathy and concrete small-step suggestions. Avoid platitudes.",
    "joy": "Respond positively and encourage sharing more about what's good.",
    "anger": "Respond calmly, acknowledge the frustration, and offer grounding techniques.",
    "fear": "Respond reassuringly and offer safety or step-by-step calming actions.",
    "love": "Respond warmly and validate the feelings.",
    "surprise": "Respond with curiosity and gentle questions."
}

app = FastAPI(title="MindMate — Emotion-conditioned Mental Health Chatbot API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory conversation memory per session_id: list of dicts [{"user":..., "bot":...}, ...]
CONVERSATION_MEMORY = {}
MAX_MEMORY = 5  # keep last 3-5 exchanges

# Initialize enhanced crisis detector
crisis_detector = get_detector(region="india")

# Pydantic request / response
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    emotion: str
    response: str
    crisis: bool = False

# Load models (try local fine-tuned; otherwise fallback)
def load_emotion_model():
    if os.path.isdir(EMOTION_MODEL_DIR):
        model_name = EMOTION_MODEL_DIR
    else:
        model_name = DEFAULT_EMOTION_MODEL
    print("Loading emotion model:", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    # if returned model outputs have different label order than expected, you'll need label mapping
    return tokenizer, model

def load_response_model():
    if os.path.isdir(RESPONSE_MODEL_DIR):
        model_name = RESPONSE_MODEL_DIR
    else:
        model_name = DEFAULT_RESPONSE_MODEL
    print("Loading response model:", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # make sure tokenizer.pad_token is set
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        model.resize_token_embeddings(len(tokenizer))
    return tokenizer, model

EMO_TOKENIZER, EMO_MODEL = load_emotion_model()
RESP_TOKENIZER, RESP_MODEL = load_response_model()

# If emotion model labels are unknown, use common order for dair-ai/emotion
EMOTION_LABELS = ["anger", "fear", "joy", "love", "sadness", "surprise"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EMO_MODEL.to(device)
RESP_MODEL.to(device)

def detect_crisis(text: str) -> tuple:
    """Use enhanced crisis detector. Returns (is_crisis, level, message)"""
    is_crisis, level, explanation = crisis_detector.detect(text)
    if is_crisis:
        message = crisis_detector.get_crisis_message(level)
        return True, level, message
    return False, None, None

def detect_emotion(text: str) -> str:
    inputs = EMO_TOKENIZER(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        logits = EMO_MODEL(**inputs).logits
    probs = torch.nn.functional.softmax(logits, dim=-1)
    label_id = int(torch.argmax(probs, dim=-1)[0])
    if label_id < len(EMOTION_LABELS):
        return EMOTION_LABELS[label_id]
    else:
        return "neutral"

def get_context(session_id: str) -> str:
    items = CONVERSATION_MEMORY.get(session_id, [])
    lines = []
    for e in items[-MAX_MEMORY:]:
        lines.append(f"User: {e['user']}\nBot: {e['bot']}")
    return "\n".join(lines)

def add_memory(session_id: str, user_text: str, bot_text: str):
    lst = CONVERSATION_MEMORY.setdefault(session_id, [])
    lst.append({"user": user_text, "bot": bot_text})
    # trim
    if len(lst) > MAX_MEMORY:
        CONVERSATION_MEMORY[session_id] = lst[-MAX_MEMORY:]

def generate_response_with_tone(user_text: str, emotion: str, context: str) -> str:
    # Build prompt for the response model
    tone_instruction = TONE_GUIDELINES.get(emotion, "Respond empathetically.")
    prompt = f"{tone_instruction}\nEmotion: {emotion}\nContext: {context}\nUser: {user_text}\nBot:"
    input_ids = RESP_TOKENIZER.encode(prompt + RESP_TOKENIZER.eos_token, return_tensors="pt").to(device)
    # generation params with repetition prevention
    with torch.no_grad():
        out = RESP_MODEL.generate(
            input_ids,
            max_length=input_ids.shape[-1] + 80,  # Reduced from 120 to prevent long repetitive outputs
            do_sample=True,
            top_p=0.92,
            top_k=50,
            temperature=0.85,
            pad_token_id=RESP_TOKENIZER.pad_token_id,
            eos_token_id=RESP_TOKENIZER.eos_token_id,
            num_return_sequences=1,
            no_repeat_ngram_size=3,  # Prevents repeating 3-word sequences
            repetition_penalty=1.2,  # Penalizes repetition
        )
    # decode only the newly generated tokens
    generated = out[0][input_ids.shape[-1]:]
    reply = RESP_TOKENIZER.decode(generated, skip_special_tokens=True).strip()
    # fallback in case model outputs nothing
    if not reply:
        reply = "Thank you for telling me. I'm here to listen — would you like to tell me more?"
    return reply

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.session_id
    user_text = req.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")

    # Crisis check with enhanced detector
    is_crisis, crisis_level, crisis_msg = detect_crisis(user_text)
    if is_crisis:
        # Still save to memory for context
        add_memory(session_id, user_text, crisis_msg)
        return ChatResponse(session_id=session_id, emotion="crisis", response=crisis_msg, crisis=True)

    # Emotion detection
    try:
        emotion = detect_emotion(user_text)
    except Exception as e:
        # fallback if model errors
        emotion = "neutral"

    # Get context from memory
    context = get_context(session_id)

    # Generate response conditioned on emotion + tone
    try:
        reply = generate_response_with_tone(user_text, emotion, context)
    except Exception as e:
        # fallback simpler behavior
        reply = "I'm sorry, I couldn't think of a good response right now. Tell me more about how you're feeling."
    
    # Save to memory
    add_memory(session_id, user_text, reply)

    return ChatResponse(session_id=session_id, emotion=emotion, response=reply, crisis=False)


@app.get("/health")
def health():
    return {"status": "ok"}
