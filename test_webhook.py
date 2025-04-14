import requests
import json

payload = {
    "symbol": "SOL/USDT",
    "price": "130.20",
    "volume": "2",
    "time": "2025-04-13T23:00:00Z",
    "strategy": "Golden Cross Explosivo v1.9",
    "signal": "buy",
    "source": "Manual",
    "note": "Teste real no sandbox Bybit"
}

url = "https://omegaexecutormododeus-mktgov.replit.app/webhook"

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)
