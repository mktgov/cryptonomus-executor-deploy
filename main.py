from flask import Flask, request, jsonify
from omega_executor.trade_logic import handle_trade

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔔 Webhook recebido:", data)

    try:
        result = handle_trade(data)
        return jsonify({"message": "Webhook recebido!", "result": result})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
