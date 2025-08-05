import os
import unittest
from unittest.mock import patch, MagicMock

import dotenv
from atlas_vector_search import run_atlas_vector_search

class TestAtlasVectorSearch(unittest.TestCase):
    @patch("atlas_vector_search.MongoClient")
    @patch("atlas_vector_search.SentenceTransformer")
    def test_run_atlas_vector_search(self, mock_model_class, mock_mongo_client):
        # Mock MongoDB aggregate results
        mock_collection = MagicMock()
        mock_aggregate_result = [
            {"_id": 1, "text": "Sports headline", "label": "sports", "score": 0.99},
            {"_id": 2, "text": "Tech news", "label": "tech", "score": 0.95},
        ]
        mock_collection.aggregate.return_value = mock_aggregate_result
        mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        # Mock SentenceTransformer
        mock_model = MagicMock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3]]
        mock_model_class.return_value = mock_model

        # Run the function
        import dotenv
        dotenv.load_dotenv()
        mongo_url = os.getenv("MONGO_URL")
        results = run_atlas_vector_search("Atlanta Braves", mongo_url)

        # Assertions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["label"], "sports")
        self.assertEqual(results[1]["label"], "tech")

if __name__ == "__main__":
    unittest.main()