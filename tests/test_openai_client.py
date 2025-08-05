import unittest
from unittest.mock import patch, MagicMock
import os

from openai_client import OpenAIClient, build_prompt

class TestOpenAIClient(unittest.TestCase):
    @patch.dict(os.environ, {
        "USE_AZURE_OPENAI": "false",
        "OPENAI_API_KEY": "fake-key"
    })
    @patch("openai_client.OpenAI")
    def test_openai_client_get_response(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient(model="gpt-4o")
        messages = [{"role": "user", "content": "Hello"}]
        response = client.get_response(messages)

        mock_client.chat.completions.create.assert_called_once()
        self.assertEqual(response.choices[0].message.content, "Test response")

    def test_build_prompt(self):
        prompt = build_prompt("Japan")
        self.assertIn("Japan", prompt)

if __name__ == "__main__":
    unittest.main()
    