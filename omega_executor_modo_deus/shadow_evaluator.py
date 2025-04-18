# omega_executor/shadow_evaluator.py

import os
import json

CRIT_MIN_TRADES = 20
CRIT_MIN_ACURACIA = 0.6
CRIT_MIN_ROI = 1.8

LOG_DIR = "logs/shadow/"
OUTPUT_FILE = "promoted_setups.json"


def avaliar_setup(setup):
    log_path = os.path.join(LOG_DIR, f"{setup}.log")
    if not os.path.exists(log_path):
        return None

    wins, losses, total_roi = 0, 0, 0
    with open(log_path, "r", encoding="utf-8") as f:
        linhas = [json.loads(l) for l in f.readlines()]

    for linha in linhas:
        if linha["resultado"] == "win":
            wins += 1
        else:
            losses += 1
        total_roi += float(linha["roi"])

    total = wins + losses
    if total < CRIT_MIN_TRADES:
        return None

    acuracia = wins / total
    roi_medio = total_roi / total

    if acuracia >= CRIT_MIN_ACURACIA and roi_medio >= CRIT_MIN_ROI:
        return {
            "setup": setup,
            "acuracia": round(acuracia, 2),
            "roi_medio": round(roi_medio, 2),
            "trades": total
        }
    return None


def avaliar_todos():
    promovidos = {}
    for arquivo in os.listdir(LOG_DIR):
        if arquivo.endswith(".log"):
            nome = arquivo.replace(".log", "")
            resultado = avaliar_setup(nome)
            if resultado:
                promovidos[nome] = resultado

    if promovidos:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(promovidos, f, indent=2, ensure_ascii=False)
        print(f"[✅] {len(promovidos)} setup(s) promovidos para {OUTPUT_FILE}")
    else:
        print("[⚠️] Nenhum setup qualificado para promoção.")


if __name__ == "__main__":
    avaliar_todos()
