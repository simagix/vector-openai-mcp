"""
sbert_vector_search.py
@ken.chen

Performs local semantic vector search on a MongoDB collection using sentence-transformers and PyTorch.
Encodes queries and documents, computes dot product similarity, and returns the top matching results.

Usage:
    python sbert_vector_search.py --mongo_url <MONGODB_URI> "Your query text here"

If --mongo_url is omitted, it defaults to the MONGO_URL environment variable or localhost.
"""

import argparse, dotenv, os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import torch

def run_local_vector_search(query_text, mongo_url, top_k=5) -> list:
    """
    Runs a local vector search using dot product similarity between a query
    and stored embeddings in MongoDB.

    Args:
        query_text (str): The input query string to search for.
        mongo_url (str): MongoDB connection URI.
        top_k (int): Number of top results to return (default = 5).
    """
    # Connect to MongoDB and access the 'ag_news' collection
    client = MongoClient(mongo_url)
    db = client["testdb"]
    collection = db["ag_news"]

    # Load sentence-transformers model and detect CUDA if available
    model = SentenceTransformer("all-MiniLM-L6-v2")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Encode the query into an embedding and move to the correct device
    query_embedding = model.encode(query_text, convert_to_tensor=True).to(device)

    # Load all documents with precomputed embeddings from MongoDB
    docs = list(collection.find({}, {"_id": 1, "text": 1, "label": 1, "embedding": 1}))
    corpus_embeddings = torch.tensor([doc["embedding"] for doc in docs]).to(device)

    # Compute dot product similarity scores
    scores = query_embedding @ corpus_embeddings.T  # Shape: (N,)

    # Retrieve top-k results based on scores
    k = min(top_k, scores.shape[-1])
    top_results = torch.topk(scores, k=k)
    
    top_indices = top_results.indices.cpu().numpy()
    top_scores = top_results.values.cpu().numpy()

    # Print results
    print(f"\nTop {k} local results for query: \"{query_text}\"")
    headlines = []
    for idx, score in zip(top_indices, top_scores):
        doc = docs[idx]
        item = {"text": doc["text"], "label": doc["label"], "score": float(score)}
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
    headlines = run_local_vector_search(args.query_text, mongo_url)
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline['text']} (score: {headline['score']:.4f})")

