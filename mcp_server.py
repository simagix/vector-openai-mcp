"""
mcp_server.py
@ken.chen

Implements the server component for the MCP (Multi-Component Pipeline) demo.
Handles incoming client requests, processes them, and returns results.

Usage:
    python mcp_server.py
"""

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
            "name": "find_report",
            "description": "Find a report related to user's input",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The report name"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_course",
            "description": "Search courses by title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The keyword or title to search"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_engineers_by_skill",
            "description": "Find engineers with a particular skill",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill": {
                        "skill": "string",
                        "description": "The name of the skill"
                    }
                },
                "required": ["skill"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_engineer_by_name",
            "description": "Find engineer by full name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The full name of the engineer"
                    }
                },
                "required": ["name"]
            }
        }
    }
]

# === Tool Functions ===
def find_report(title):
    return f"Found a report for {title}"

def find_course(title):
    return f"Found courses related to '{title}'"

def find_engineers_by_skill(skill):
    return f"Found engineers skilled in '{skill}' include: Alice, Bob, Charlie"

def find_engineer_by_name(name):
    return f"Found engineer info for '{name}': Region: AMER, Skills: MongoDB, Python"

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

        # Route to function
        if name == "find_report":
            result = find_report(**args)
        elif name == "find_course":
            result = find_course(**args)
        elif name == "find_engineers_by_skill":
            result = find_engineers_by_skill(**args)
        elif name == "find_engineer_by_name":
            result = find_engineer_by_name(**args)
        else:
            result = "Unknown tool"

        return jsonify({"tool": name, "arguments": args, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
