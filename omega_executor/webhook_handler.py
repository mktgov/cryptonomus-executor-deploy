from flask import Flask, request
import os
import requests

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook_listener():
    data = request.json
    print("🚨 Webhook recebido:", data)

    # Telegram alert
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = f"⚡ Alerta recebido: {data.get('symbol', 'N/A')} | Estratégia: {data.get('strategy', 'N/A')}"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)

    print("✅ Telegram:", response.json())

    return {"status": "received"}, 200
