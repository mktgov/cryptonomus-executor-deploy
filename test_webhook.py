import requests
import json

url = "https://82e9e3ee-dd95-4eb9-8260-d0881a88b405-00-11m9hhvza3vl0.kirk.replit.dev/"

payload = {
    "symbol": "ETHUSDT",
    "price": "1825.20",
    "volume": "153000000",
    "time": "2025-04-13T23:00:00Z",
    "strategy": "Teste direto",
    "signal": "buy",
    "source": "Manual",
    "note": "Simulação de alerta"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.text)
