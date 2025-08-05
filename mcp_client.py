"""
mcp_client.py
@ken.chen

Implements the client component for the MCP (Multi-Component Pipeline) demo.
Sends requests to the MCP server and displays the responses.

Usage:
    python mcp_client.py "Your question here"
    # or just
    python mcp_client.py
    # and enter your question interactively
"""

import requests, sys

def send_request(user_input):
    url = "http://localhost:5000/mcp"
    payload = {"input": user_input}
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        user_query = input("Ask something: ")
    else:
        user_query = " ".join(sys.argv[1:])
    
    data = send_request(user_query)

    if "data" in data:
        for i, headline in enumerate(data["data"], start=1):
            print(i, headline)
    else:
        print(data)
