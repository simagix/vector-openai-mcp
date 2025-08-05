"""
load_data.py
@ken.chen

This script loads the AG News dataset, generates sentence-transformer embeddings,
and stores them in a MongoDB collection along with the original text and label.

Usage:
    python load_data.py
    python load_data.py --mongo_url mongodb://host:port --limit 500

Defaults:
    mongo_url: from MONGO_URL env variable or localhost
    limit: 1000 documents
"""

import argparse, dotenv, os
from datasets import load_dataset
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

def load_and_store_vector_data(mongo_url: str, limit: int = 1000):
    # Load dataset
    dataset = load_dataset("ag_news", split=f"train[:{limit}]")
    docs = [{"_id": i, "text": item["text"], "label": item["label"]} for i, item in enumerate(dataset)]

    # Connect to MongoDB
    client = MongoClient(mongo_url)
    db = client["testdb"]
    collection = db["ag_news"]

    # Clear old data
    collection.delete_many({})

    # Generate embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [doc["text"] for doc in docs]
    embeddings = model.encode(texts).tolist()

    for i, embedding in enumerate(embeddings):
        docs[i]["embedding"] = embedding

    # Insert into MongoDB
    collection.insert_many(docs)
    print(f"Inserted {len(docs)} documents with embeddings into 'ag_news' collection.")

if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="Load and store vector data into MongoDB")
    parser.add_argument("--mongo_url", help="MongoDB URI (optional, defaults to env MONGO_URL or localhost)")
    parser.add_argument("--limit", type=int, default=1000, help="Number of samples to load from the dataset")
    args = parser.parse_args()

    mongo_url = args.mongo_url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    load_and_store_vector_data(mongo_url, args.limit)
