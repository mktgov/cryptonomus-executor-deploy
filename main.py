from flask import Flask, request, jsonify
from omega_executor.trade_logic import handle_trade
from notifier import enviar_alerta
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "omega_executor",
                     "omega_executor")))

import os
import os
import hmac
import hashlib
import json

app = Flask(__name__)


def verificar_assinatura(payload, assinatura_recebida):
    """
    Garante que a requisição veio de fonte autorizada.
    """
    secret = os.getenv("AUTH_SECRET", "")
    corpo = json.dumps(payload, separators=(",", ":")).encode()
    assinatura_calculada = hmac.new(secret.encode(), corpo,
                                    hashlib.sha256).hexdigest()
    return hmac.compare_digest(assinatura_calculada, assinatura_recebida)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "CRYPTONOMUS EXECUTOR ONLINE"}), 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    assinatura = request.headers.get("X-AUTH", "")

    if not verificar_assinatura(data, assinatura):
        print("🚨 Assinatura inválida!")
        return jsonify({"message": "Unauthorized"}), 403

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
