# fine_tune_response.py
"""
Fine-tune DialoGPT to respond with emotion+context conditioning.
Saves model/tokenizer to ./models/response_model

Run:
    python fine_tune_response.py
"""

import os
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments)
from transformers import DataCollatorForLanguageModeling
import math

MODEL_NAME = "microsoft/DialoGPT-small"
OUT_DIR = "./models/response_model"
MAX_LENGTH = 128

def build_prompt(example):
    # Handle different dataset formats
    try:
        # Facebook EmpatheticDialogues format (has 'prompt', 'utterance', 'context')
        if "prompt" in example and "utterance" in example:
            ctx = example.get("prompt", "")
            emotion = example.get("context", "neutral")  # 'context' field contains emotion label
            response = example.get("utterance", "")
            user_text = ctx
        # Alternative EmpatheticDialogues format
        elif "context" in example and isinstance(example.get("context"), (list, str)):
            ctx = " ".join(example["context"]) if isinstance(example["context"], list) else example["context"]
            emotion = example.get("emotion", "neutral")
            response = example.get("response", example.get("utterance", ""))
            user_text = ctx.split("\n")[-1] if ctx else ""
        # DailyDialog format
        elif "dialog" in example:
            dialog = example["dialog"]
            if len(dialog) >= 2:
                ctx = " ".join(dialog[:-1])
                response = dialog[-1]
                user_text = dialog[-2] if len(dialog) >= 2 else ""
            else:
                ctx = ""
                response = dialog[0] if dialog else ""
                user_text = ""
            emotion = example.get("emotion", ["neutral"])[0] if "emotion" in example else "neutral"
        # Generic format
        else:
            ctx = example.get("text", "")
            response = example.get("response", example.get("completion", ""))
            emotion = example.get("emotion", "neutral")
            user_text = ctx
        
        # Prompt format: Emotion: <emotion>\nUser: <user_text>\nBot: <response>
        prompt = f"Emotion: {emotion}\nUser: {user_text}\nBot: {response}"
        return prompt
    except Exception as e:
        print(f"Error processing example: {e}")
        return "Emotion: neutral\nUser: \nBot: "

def preprocess_dataset(dataset):
    prompts = []
    for ex in dataset:
        prompts.append(build_prompt(ex))
    return prompts

def chunk_and_tokenize(prompts, tokenizer):
    encodings = tokenizer(prompts, truncation=True, padding=True, max_length=MAX_LENGTH)
    return encodings

def create_synthetic_dataset():
    """Create a synthetic empathetic dialogue dataset"""
    from datasets import Dataset
    
    emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'love']
    
    # Sample synthetic dialogues
    synthetic_data = []
    templates = [
        ("I just got promoted at work!", "That's wonderful news! Congratulations on your promotion!", "joy"),
        ("I'm feeling really down today.", "I'm sorry to hear that. Is there anything I can do to help?", "sadness"),
        ("This is so frustrating!", "I understand your frustration. Let's see if we can work through this together.", "anger"),
        ("I'm worried about the exam tomorrow.", "It's natural to feel nervous. You've prepared well, try to stay positive.", "fear"),
        ("I can't believe I won the lottery!", "Wow, that's amazing! What a surprise!", "surprise"),
        ("I really appreciate everything you do for me.", "That means a lot to me. I'm happy to be here for you.", "love"),
        ("My dog passed away yesterday.", "I'm so sorry for your loss. Losing a pet is incredibly difficult.", "sadness"),
        ("I'm so excited about the concert tonight!", "That sounds fantastic! I hope you have an amazing time!", "joy"),
        ("Why does this always happen to me?", "I can see why you're upset. Sometimes life can be really challenging.", "anger"),
        ("I'm scared about the surgery.", "It's completely understandable to feel scared. The doctors will take good care of you.", "fear"),
    ]
    
    # Expand the dataset
    for i in range(500):  # Create 500 training examples
        prompt, response, emotion = templates[i % len(templates)]
        synthetic_data.append({
            "prompt": prompt,
            "utterance": response,
            "context": emotion
        })
    
    return Dataset.from_dict({
        "prompt": [d["prompt"] for d in synthetic_data],
        "utterance": [d["utterance"] for d in synthetic_data],
        "context": [d["context"] for d in synthetic_data]
    })

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("=" * 70)
    print("Loading REAL Mental Health Counseling Dataset from local file...")
    print("=" * 70)
    
    # Check if dataset file exists
    dataset_file = "./dataset/mental_health_counseling.json"
    if not os.path.exists(dataset_file):
        print("\n❌ ERROR: Dataset file not found!")
        print(f"   Expected: {dataset_file}")
        print("\n➜ Please run first: python download_dataset.py")
        print("=" * 70)
        return
    
    # Load from local JSON file
    import json
    with open(dataset_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Loaded {len(data)} real counseling conversations!")
    
    # Split into train/validation (90/10)
    split_idx = int(len(data) * 0.9)
    train_data = data[:split_idx]
    val_data = data[split_idx:]
    
    print(f"\nTraining set: {len(train_data)} examples")
    print(f"Validation set: {len(val_data)} examples")
    
    # Convert to training prompts
    print("\nConverting to training format...")
    train_prompts = []
    for example in train_data:
        context = example['context']
        response = example['response']
        # Simple prompt format for mental health conversations
        prompt = f"User: {context}\nBot: {response}"
        train_prompts.append(prompt)
    
    val_prompts = []
    for example in val_data:
        context = example['context']
        response = example['response']
        prompt = f"User: {context}\nBot: {response}"
        val_prompts.append(prompt)
    
    print(f"✅ Created {len(train_prompts)} training prompts!")

    print("Loading tokenizer & model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # ensure tokenizer has pad token
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.resize_token_embeddings(len(tokenizer))

    print("Tokenizing...")
    train_enc = tokenizer(train_prompts, truncation=True, padding=True, max_length=MAX_LENGTH)
    val_enc = tokenizer(val_prompts, truncation=True, padding=True, max_length=MAX_LENGTH)

    # convert to dataset objects (datasets.Dataset)
    from datasets import Dataset
    train_dataset = Dataset.from_dict(train_enc)
    val_dataset = Dataset.from_dict(val_enc)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir="./runs/response",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=8,
        eval_steps=500,
        eval_strategy="steps",
        save_steps=1000,
        save_total_limit=2,
        learning_rate=5e-5,
        logging_steps=100,
        fp16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )

    print("\n" + "=" * 70)
    print("Starting Training on REAL Mental Health Data...")
    print("=" * 70)
    print("Training Details:")
    print(f"  - Dataset: Amod/mental_health_counseling_conversations")
    print(f"  - Training examples: {len(train_prompts)}")
    print(f"  - Validation examples: {len(val_prompts)}")
    print(f"  - Epochs: 3")
    print(f"  - Model: {MODEL_NAME}")
    print(f"\nThis will take approximately 30-60 minutes...")
    print("You'll see much better responses than synthetic data!")
    print("=" * 70 + "\n")
    
    trainer.train()
    
    print("\n" + "=" * 70)
    print("✅ Training Complete!")
    print("=" * 70)
    print(f"Saving model to: {OUT_DIR}")
    
    trainer.save_model(OUT_DIR)
    tokenizer.save_pretrained(OUT_DIR)
    
    print("\n✅ Model saved successfully!")
    print("\nNext steps:")
    print("  1. Restart your backend server")
    print("  2. Test the chatbot")
    print("  3. Responses should be MUCH better now!")
    print("=" * 70)

if __name__ == "__main__":
    main()
