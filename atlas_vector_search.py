"""
atlas_vector_search.py
@ken.chen

Performs semantic vector search on a MongoDB Atlas collection using Atlas Search's $vectorSearch operator.
Encodes queries with SentenceTransformer and retrieves the most similar documents from the database.

Usage:
    python atlas_vector_search.py --mongo_url <MONGODB_ATLAS_URI> "Your query text here"

If --mongo_url is omitted, it defaults to the MONGO_URL environment variable or localhost.
"""

import argparse, dotenv, os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

def run_atlas_vector_search(query_text, mongo_url) -> list:
    # Connect to MongoDB
    client = MongoClient(mongo_url)
    db = client["testdb"]
    collection = db["ag_news"]

    # Load model and encode query
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vector = list(model.encode([query_text])[0])

    # Perform vector search using Atlas Search
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": 5,
                "similarity": "dotProduct"
            }
        },
        {
            "$project": {
                "_id": 1,
                "text": 1,
                "label": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ])

    headlines = []
    for doc in results:
        item = {"text": doc["text"], "label": doc["label"], "score": float(doc['score'])}
        headlines.append(item)
    
    return headlines

if __name__ == "__main__":
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser(description="Run local vector search with sentence-transformers")
    parser.add_argument("--mongo_url", help="MongoDB connection URI (optional, defaults to env MONGO_URL or localhost)")
    parser.add_argument("query_text", nargs="?", default="Breaking news about sports",
                        help="Query text to search for (default: 'Breaking news about sports')")
    args = parser.parse_args()

    # Resolve MongoDB connection string
    mongo_url = args.mongo_url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")

    # Execute vector search
    headlines = run_atlas_vector_search(args.query_text, mongo_url)
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline['text']} (score: {headline['score']:.4f})")
