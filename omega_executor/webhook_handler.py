from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Payload recebido:", data)
    return jsonify({
        "status": "sucesso",
        "message": "Webhook processado com sucesso"
    }), 200
