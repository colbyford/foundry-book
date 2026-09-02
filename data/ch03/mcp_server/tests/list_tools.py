import requests

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}

response = requests.post(
    "http://localhost:8000/mcp",
    json=payload,
    headers={"Content-Type": "application/json"}
)

response.raise_for_status()
result = response.json()

for tool in result["result"]["tools"]:
    print(tool["name"], "-", tool.get("description"))
