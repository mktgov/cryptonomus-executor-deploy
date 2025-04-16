from flask import Flask, request, jsonify
from omega_executor.trade_logic import handle_trade
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "CRYPTONOMUS EXECUTOR ONLINE"}), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("⚠️ Webhook recebido:", data)

    try:
        result = handle_trade(data)
        return jsonify({"message": "Webhook recebido!", "result": result}), 200
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 CRYPTONOMUS ONLINE na porta {port}")
    app.run(host="0.0.0.0", port=port)
