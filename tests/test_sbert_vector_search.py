import unittest
from unittest.mock import patch, MagicMock
import torch
from sbert_vector_search import run_local_vector_search

class TestSbertVectorSearch(unittest.TestCase):
    @patch("sbert_vector_search.MongoClient")
    @patch("sbert_vector_search.SentenceTransformer")
    def test_run_local_vector_search(self, mock_model_class, mock_mongo_client):
        # Setup mock MongoDB documents
        mock_collection = MagicMock()
        mock_docs = [
            {"_id": 1, "text": "News about sports", "label": "sports", "embedding": [0.1, 0.2, 0.3]},
            {"_id": 2, "text": "Breaking tech update", "label": "tech", "embedding": [0.4, 0.5, 0.6]},
            {"_id": 3, "text": "Politics today", "label": "politics", "embedding": [0.7, 0.8, 0.9]},
        ]
        mock_collection.find.return_value = mock_docs
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        # Setup mock model
        mock_model = MagicMock()
        mock_query_embedding = torch.tensor([0.1, 0.2, 0.3])
        mock_model.encode.return_value = mock_query_embedding
        mock_model_class.return_value = mock_model

        # Run search
        results = run_local_vector_search("sports news", "mongodb://localhost:27017/testdb")

        # Verify the results structure and mock calls
        self.assertEqual(len(results), 3)
        for res in results:
            self.assertIn("text", res)
            self.assertIn("label", res)
            self.assertIn("score", res)
            self.assertIsInstance(res["score"], float)

if __name__ == "__main__":
    unittest.main()
