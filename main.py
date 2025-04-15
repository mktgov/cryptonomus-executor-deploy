from flask import Flask, request, jsonify
from omega_executor.trade_logic import handle_trade
import os

app = Flask(__name__)


# ✅ Healthcheck para Render
@app.route("/", methods=["GET"])
def index():
    return "I'M ALIVE", 200


# ✅ Webhook para receber sinais
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return jsonify({"message": "OK"}), 200

    data = request.get_json()
    print("⚠️ Webhook recebido:", data)

    try:
        result = handle_trade(data)
        return jsonify({"message": "Webhook recebido!", "result": result})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


# 👇 EXECUÇÃO OBRIGATÓRIA PARA RENDER FUNCIONAR
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🔥 CRYPTONOMUS EXECUTOR ONLINE na porta {port}")
    app.run(host="0.0.0.0", port=port)
