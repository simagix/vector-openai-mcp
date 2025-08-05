import unittest
import subprocess
import time
import requests

class TestMcpIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server
        cls.server = subprocess.Popen(
            ["python", "mcp_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Wait for server to start (adjust as needed)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait()

    def test_client_server_interaction(self):
        # Example: If mcp_client.py prints the result, capture it
        result = subprocess.run(
            ["python", "mcp_client.py", "--query", "test"],
            capture_output=True,
            text=True
        )
        self.assertIn("{'arguments': {'title': 'test'}, 'result': 'Found a report for test', 'tool': 'find_report'}\n", result.stdout)

if __name__ == "__main__":
    unittest.main()