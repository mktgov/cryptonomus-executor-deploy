import requests
import os

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
msg = "✅ Executor online: comunicação com Telegram validada com sucesso."

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {"chat_id": chat_id, "text": msg}

response = requests.post(url, data=payload)

print("Status:", response.status_code)
print("Resposta:", response.json())
