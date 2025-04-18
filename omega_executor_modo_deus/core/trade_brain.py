# omega_executor/trade_brain.py

import json
import os
from collections import defaultdict

CAMINHO = "logs/brain_stats.json"


def carregar_brain():
    if not os.path.exists(CAMINHO):
        return defaultdict(lambda: {"win": 0, "loss": 0})

    with open(CAMINHO, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return defaultdict(lambda: {"win": 0, "loss": 0})


def salvar_brain(data):
    with open(CAMINHO, "w") as f:
        json.dump(data, f, indent=2)


def registrar_resultado_brain(strategy, result):
    brain = carregar_brain()
    if strategy not in brain:
        brain[strategy] = {"win": 0, "loss": 0}

    if result not in ["win", "loss"]:
        return  # ignora qualquer outro

    brain[strategy][result] += 1
    salvar_brain(brain)


def avaliar_setup_brain(strategy):
    brain = carregar_brain()
    stats = brain.get(strategy, {"win": 0, "loss": 0})
    total = stats["win"] + stats["loss"]

    if total < 10:
        return True  # precisa de mais dados para avaliar

    taxa = stats["win"] / total
    return taxa >= 0.65  # exige 65%+ de winrate
