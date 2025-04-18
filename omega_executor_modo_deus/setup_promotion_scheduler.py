# omega_executor/setup_promotion_scheduler.py (atualizado com despromoção)

import os
import json
import time
from statistics import mean

SHADOW_DIR = "logs/shadow"
PROMOTED_PATH = "logs/promoted_setups.json"
BANIDOS_PATH = "logs/banned_setups.log"

# Critérios de promoção
MIN_TRADES = 20
MIN_ACURACIA = 0.6
MIN_ROI = 1.8

# Critérios de despromoção
DROP_ACURACIA = 0.5
DROP_ROI = 1.2


def avaliar_setup(setup_name, logs):
    if len(logs) < MIN_TRADES:
        return None

    wins = sum(1 for l in logs if l["resultado"] == "win")
    acuracia = wins / len(logs)
    roi_medio = mean([l["roi"] for l in logs])

    return {
        "setup": setup_name,
        "trades": len(logs),
        "acuracia": round(acuracia * 100, 2),
        "roi_medio": round(roi_medio, 2),
        "fase": logs[-1]["fase"]
    }


def carregar_logs_shadow(setup):
    caminho = os.path.join(SHADOW_DIR, f"{setup}.log")
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f.readlines() if l.strip()]


def promover_setup(dados):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    promovidos = {}
    if os.path.exists(PROMOTED_PATH):
        with open(PROMOTED_PATH, "r", encoding="utf-8") as f:
            promovidos = json.load(f)

    promovidos[dados["setup"]] = {
        "fase": dados["fase"],
        "acuracia": dados["acuracia"],
        "roi_medio": dados["roi_medio"],
        "trades": dados["trades"]
    }

    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        json.dump(promovidos, f, ensure_ascii=False, indent=2)
    print(f"[⚔️] Setup promovido: {dados['setup']}")


def despromover_setups():
    if not os.path.exists(PROMOTED_PATH):
        return

    with open(PROMOTED_PATH, "r", encoding="utf-8") as f:
        promovidos = json.load(f)

    atualizados = promovidos.copy()
    for setup in promovidos:
        logs = carregar_logs_shadow(setup)
        if len(logs) < MIN_TRADES:
            continue

        avaliacao = avaliar_setup(setup, logs)
        if not avaliacao:
            continue

        if (avaliacao["acuracia"] /
                100) < DROP_ACURACIA or avaliacao["roi_medio"] < DROP_ROI:
            atualizados.pop(setup)
            motivo = f"Despromovido: {setup} | Acuracia: {avaliacao['acuracia']} | ROI: {avaliacao['roi_medio']}"
            print("[⚠️] ", motivo)
            with open(BANIDOS_PATH, "a", encoding="utf-8") as ban:
                ban.write(motivo + "\n")

    with open(PROMOTED_PATH, "w", encoding="utf-8") as f:
        json.dump(atualizados, f, ensure_ascii=False, indent=2)


def verificar_promocao():
    print("\n[🔍] Verificando setups shadow...")
    for nome_arquivo in os.listdir(SHADOW_DIR):
        if not nome_arquivo.endswith(".log"):
            continue
        setup = nome_arquivo.replace(".log", "")
        logs = carregar_logs_shadow(setup)
        avaliacao = avaliar_setup(setup, logs)
        if not avaliacao:
            continue
        if (avaliacao["acuracia"] /
                100) >= MIN_ACURACIA and avaliacao["roi_medio"] >= MIN_ROI:
            promover_setup(avaliacao)

    despromover_setups()


if __name__ == "__main__":
    while True:
        verificar_promocao()
        print("[⏱️] Próxima avaliação em 1 hora...")
        time.sleep(3600)
