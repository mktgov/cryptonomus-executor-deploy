# omega_executor/setup_guard.py

import json
import os

HISTORICO_PATH = "logs/historico_setups.json"
PROMOVIDOS_PATH = "promoted_setups.json"

SETUPS_APROVADOS_INICIAIS = {
    "Golden Cross Explosivo": 0.72,
    "Break + Retest": 0.75,
    "Capitulacao RSI": 0.68,
    "Reversão Suporte Major": 0.7
}

FILTRO_MIN_ACURACIA = 0.6

# Carrega setups promovidos
try:
    with open(PROMOVIDOS_PATH, "r", encoding="utf-8") as f:
        SETUPS_PROMOVIDOS = json.load(f)
except FileNotFoundError:
    SETUPS_PROMOVIDOS = {}


def setup_permitido(setup_nome):
    if setup_nome in SETUPS_PROMOVIDOS:
        return True
    return SETUPS_APROVADOS_INICIAIS.get(setup_nome, 0) >= FILTRO_MIN_ACURACIA


def registrar_execucao(setup_nome, resultado, fase=None, roi=0):
    os.makedirs("logs", exist_ok=True)

    historico = {}
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            historico = json.load(f)

    if setup_nome not in historico:
        historico[setup_nome] = {}
    if fase not in historico[setup_nome]:
        historico[setup_nome][fase] = {"trades": 0, "wins": 0, "roi_total": 0}

    historico[setup_nome][fase]["trades"] += 1
    if resultado == "win":
        historico[setup_nome][fase]["wins"] += 1
    historico[setup_nome][fase]["roi_total"] += roi

    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)
