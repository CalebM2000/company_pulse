import pandas as pd, numpy as np, random, time, json
from datetime import datetime
from textblob import TextBlob
import os

os.makedirs("data", exist_ok=True)

def generate_sentiment():
    phrases = ["love this product", "terrible service", "great quality", "not worth the money"]
    text = random.choice(phrases)
    return TextBlob(text).sentiment.polarity

def generate_event():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "sales": round(random.uniform(500, 1500), 2),
        "transactions": random.randint(50, 200),
        "sentiment": generate_sentiment()
    }

if __name__ == "__main__":
    print("📡 Starting data stream... Press Ctrl+C to stop.")
    while True:
        event = generate_event()
        with open("data/live_data.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        print("✅ New event:", event)
        time.sleep(5)
