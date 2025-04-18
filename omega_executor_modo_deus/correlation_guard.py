# omega_executor/correlation_guard.py

import json
import os
from datetime import datetime, timedelta

# Simula um banco de execuções recentes por ativo (poderia ser Redis, SQLite etc)
LOG_PATH = "logs/executions.json"
MAX_WINDOW_MINUTES = 30  # Janela de proteção


def carregar_execucoes():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_execucao(execucao):
    execucoes = carregar_execucoes()
    execucoes.append(execucao)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(execucoes, f, ensure_ascii=False, indent=2)


def validar_correlacoes(data):
    now = datetime.utcnow()
    ativos_bloqueados = ["BTC/USDT", "ETH/USDT",
                         "SOL/USDT"]  # Exemplo: ativos correlacionados

    execucoes = carregar_execucoes()
    recentes = [
        e for e in execucoes if datetime.fromisoformat(e["timestamp"]) > now -
        timedelta(minutes=MAX_WINDOW_MINUTES)
    ]

    sinais_correlatos = [
        e for e in recentes
        if e["symbol"] in ativos_bloqueados and e["signal"] == data["signal"]
    ]

    if sinais_correlatos:
        return False, f"Sinal semelhante já executado para ativo correlacionado nos últimos {MAX_WINDOW_MINUTES} min."

    # Registra execução se passou na validação
    salvar_execucao({
        "symbol": data["symbol"],
        "signal": data["signal"],
        "timestamp": now.isoformat()
    })

    return True, "OK"
