# webhook_handler.py
from flask import Flask, request, jsonify
from trade_logic import handle_trade  # ✅ CERTO

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook recebido:", data)

    try:
        resultado = handle_trade(data)
        return jsonify({'status': 'ok', 'resultado': resultado}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
