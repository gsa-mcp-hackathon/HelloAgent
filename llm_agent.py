
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

question = input("Enter your application question: ").strip()

prompt = f"""
You are a tool-selection assistant for HelloAgent.

Available MCP tools:
1. say_hello(name)
2. get_application(application_name)
3. list_applications()
4. list_approved_applications_by_vendor(vendor)

User question: {question}

Select the most appropriate tool.

Respond ONLY with JSON in this format:
{{
  "tool": "list_approved_applications_by_vendor",
  "arguments": {{"vendor": "Microsoft"}}
}}
"""

payload = {
    "model": MODEL,
    "prompt": prompt,
    "format": "json",
    "stream": False,
    "options": {"temperature": 0}
}

request = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(request, timeout=120) as response:
    result = json.load(response)

print("User question:", question)
print("LLM tool selection:")
print(result["response"])

import asyncio
from tool_security import validate_tool_name, validate_tool_arguments
from mcp_client import (
    get_approved_applications_by_vendor,
    get_application_list,
)
# Parse the LLM's proposed tool call.
selection = json.loads(result["response"])

# Validate the LLM-selected tool before execution.
tool_name = validate_tool_name(selection.get("tool"))
arguments = selection.get("arguments")
arguments = validate_tool_arguments(tool_name, arguments)

# Execute only the selected, validated MCP tool.
if selection["tool"] == "list_applications":
    tool_result = asyncio.run(
        get_application_list()
    )
else:
    vendor = arguments["vendor"]

    if not isinstance(vendor, str) or not vendor.strip():
        raise ValueError("Invalid vendor")

    tool_result = asyncio.run(
        get_approved_applications_by_vendor(vendor)
    )
print("\nActual MCP tool result:")
print(tool_result)

