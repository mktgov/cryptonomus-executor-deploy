# oraculo_executor.py

from oraculo_core import analisar_mercado
from setup_guard import carregar_setups_promovidos

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import hmac
import hashlib
import json

load_dotenv()


def gerar_assinatura(payload, secret):
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    return hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()


def executar_oraculo_e_disparar():
    resultado = analisar_mercado()

    # Carrega setups promovidos do arquivo json
    setups_promovidos = carregar_setups_promovidos()
    setup_usado = resultado.get("setup")

    # Verifica se setup promovido existe para fase atual e adiciona info
    setup_promovido = setups_promovidos.get(setup_usado)
    nota_promocao = ""
    if setup_promovido:
        nota_promocao = (f"[SETUP PROMOVIDO: {setup_usado}] "
                         f"ROI Médio: {setup_promovido['roi_medio']}% "
                         f"Acurácia: {setup_promovido['acuracia']}%")

    payload = {
        "symbol": resultado["ativo"],
        "side": resultado["direcao"].lower(),
        "entry": resultado["entrada"],
        "stop": resultado["stop"],
        "tps": [resultado["alvo"]],
        "risk": 2.0,
        "price": resultado["entrada"],
        "volume": 1000,
        "time": datetime.utcnow().isoformat(),
        "strategy": setup_usado,
        "signal": resultado["direcao"].lower(),
        "source": "oraculo",
        "note": f"{resultado['justificativa']} {nota_promocao}"
    }

    webhook = os.getenv("WEBHOOK_EXECUTION_URL")
    secret = os.getenv("AUTH_SECRET")

    assinatura = gerar_assinatura(payload, secret)
    headers = {"Content-Type": "application/json", "X-AUTH": assinatura}

    print("\n[🔮] PLANO ENVIADO AO EXECUTOR:")
    for k, v in payload.items():
        print(f"{k}: {v}")

    response = requests.post(webhook, json=payload, headers=headers)
    print(f"\n[📤] Enviado para {webhook} -> Status {response.status_code}")
    print("[📦] Resposta:", response.text)

    # Log local da execução
    try:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.utcnow().isoformat()
        with open("logs/execucao.log", "a") as f:
            f.write(
                f"[{timestamp}] Status {response.status_code} | {response.text}\n"
            )
    except Exception as e:
        print(f"[⚠️] Falha ao registrar log: {e}")


if __name__ == "__main__":
    executar_oraculo_e_disparar()
