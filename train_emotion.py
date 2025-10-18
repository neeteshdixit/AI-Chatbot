# train_emotion.py
"""
Fine-tune a BERT-based emotion classifier on the dair-ai/emotion dataset.
Saves model/tokenizer to ./models/emotion_detector
Run:
    python train_emotion.py
"""

import os
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          Trainer, TrainingArguments, DataCollatorWithPadding)
import numpy as np
from sklearn.metrics import accuracy_score

MODEL_NAME = "bert-base-uncased"
OUT_DIR = "./models/emotion_detector"
NUM_LABELS = 6  # dair-ai/emotion labels: anger, fear, joy, love, sadness, surprise

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Loading dataset...")
    ds = load_dataset("dair-ai/emotion")
    label_names = ds["train"].features["label"].names
    print("Labels:", label_names)

    print("Loading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)

    def preprocess(batch):
        return tokenizer(batch["text"], truncation=True)

    print("Tokenizing...")
    tokenized = ds.map(preprocess, batched=True)
    tokenized = tokenized.remove_columns(["text"])
    tokenized = tokenized.rename_column("label", "labels")
    tokenized.set_format(type="torch")

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc}

    training_args = TrainingArguments(
        output_dir="./runs/emotion",
        eval_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
        logging_steps=100
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(OUT_DIR)
    tokenizer.save_pretrained(OUT_DIR)
    print("Saved emotion model to", OUT_DIR)

if __name__ == "__main__":
    main()
