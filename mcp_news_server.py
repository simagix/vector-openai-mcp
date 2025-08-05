"""
mcp_news_server.py
@ken.chen

Implements a news-focused server component for the MCP (Multi-Component Pipeline) demo.
Receives client requests, performs news-related processing or search, and returns relevant results.

Usage:
    python mcp_news_server.py
"""

import os
from flask import Flask, request, jsonify
from openai_client import OpenAIClient
from dotenv import load_dotenv
import json

app = Flask(__name__)
load_dotenv()
agent = OpenAIClient()

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_headline_report",
            "description": "Find a report related to a user's input",
            "parameters": {
                "type": "object",
                "properties": {
                    "headline": {
                        "type": "string",
                        "description": "The news headline or topic to search for"
                    }
                },
                "required": ["headline"]
            }
        }
    }
]

# === Tool Functions ===
def find_headline_report(headline) -> list:
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    from sbert_vector_search import run_local_vector_search
    results = run_local_vector_search(query_text=headline, mongo_url=mongo_url, top_k=5)
    return results

@app.route('/mcp', methods=['POST'])
def handle_mcp():
    data = request.get_json()
    user_input = data.get("input")
    user_id = 'ken.chen' # Example user ID, replace with actual logic to get user ID
    if not user_input:
        return jsonify({"error": "Missing input"}), 400

    try:
        messages = [{"role": "user", "content": f"user_id is '{user_id}' and user_input is '{user_input}'"}]
        response = agent.get_response(messages, tools)
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"Tool call: {tool_call}")
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        headlines = []

        # Route to function
        if name == "find_headline_report":
            headlines = find_headline_report(**args)
            result = name
        else:
            result = "Unknown tool"

        return jsonify({"tool": name, "arguments": args, "result": result, "data": headlines}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
