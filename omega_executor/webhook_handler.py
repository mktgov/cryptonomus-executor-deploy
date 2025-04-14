from flask import Flask, request
import os
import requests

app = Flask(__name__)


# Função de tratamento do webhook (você pode expandir aqui)
def handle_webhook(data):
    print("📡 Webhook recebido.")
    print(data)

    # Exemplo: enviar confirmação no Telegram
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = f"📈 Alerta recebido: {data.get('symbol', 'ativo desconhecido')} | Estratégia: {data.get('strategy', 'N/A')}"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    print("Resposta do Telegram:", response.json())


@app.route('/webhook', methods=['POST'])
def webhook_listener():
    data = request.json
    handle_webhook(data)
    return {"status": "received"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
