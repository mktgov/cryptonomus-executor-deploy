from flask import Flask, request, jsonify
from omega_executor.trade_logic import handle_trade

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "CRYPTONOMUS EXECUTOR ONLINE"}), 200


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
        return jsonify({"message": str(e), "status": "error"})
