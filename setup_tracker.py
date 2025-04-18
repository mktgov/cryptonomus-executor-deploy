# omega_executor/setup_tracker.py (adição ao final)

import os
import json
from datetime import datetime

SETUPS_PATH = "data/promoted_setups.json"
ALERT_LOG = "logs/setups_em_risco.log"


def detectar_setups_em_risco():
    if not os.path.exists(SETUPS_PATH):
        return []

    with open(SETUPS_PATH, "r", encoding="utf-8") as f:
        setups = json.load(f)

    setups_em_risco = []

    for nome, dados in setups.items():
        trades = dados.get("trades", 0)
        roi = dados.get("roi_medio", 0)
        acuracia = dados.get("acuracia", 100)

        if trades >= 10 and (roi < 1.2 or acuracia < 55):
            setups_em_risco.append({
                "setup": nome,
                "roi": roi,
                "acuracia": acuracia
            })

    return setups_em_risco


def registrar_alertas_de_risco():
    setups_em_alerta = detectar_setups_em_risco()
    if not setups_em_alerta:
        return

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.utcnow().isoformat()

    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        for setup in setups_em_alerta:
            alerta = (
                f"[{timestamp}] ALERTA: Setup '{setup['setup']}' em risco - "
                f"ROI: {setup['roi']} | Acurácia: {setup['acuracia']}\n")
            f.write(alerta)
            print(f"\n✨ {alerta}")


if __name__ == "__main__":
    registrar_alertas_de_risco()
