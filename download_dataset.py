"""
Download mental health counseling dataset and save locally
"""
import os
from datasets import load_dataset
import json

print("=" * 60)
print("Downloading Mental Health Counseling Dataset...")
print("=" * 60)

# Create dataset directory
os.makedirs("./dataset", exist_ok=True)

# Download from HuggingFace
print("\nDownloading from HuggingFace...")
dataset = load_dataset("Amod/mental_health_counseling_conversations")

print(f"✅ Downloaded {len(dataset['train'])} conversations!")

# Save as JSON for easy access
output_file = "./dataset/mental_health_counseling.json"
print(f"\nSaving to {output_file}...")

# Convert to list of dictionaries
data_list = []
for example in dataset['train']:
    data_list.append({
        'context': example['Context'],
        'response': example['Response']
    })

# Save as JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data_list, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(data_list)} conversations to dataset folder!")
print("\nDataset info:")
print(f"  - File: {output_file}")
print(f"  - Size: {len(data_list)} question-answer pairs")
print(f"  - Format: JSON with 'context' and 'response' keys")
print("\n" + "=" * 60)
print("Dataset download complete!")
print("=" * 60)
