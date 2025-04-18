# omega_executor/inteligencia_preditiva.py

import os
import json
from datetime import datetime

LOG_PATH = "logs/trade_memory.log"
MAX_JANELA = 30

# Salva cada resultado com metadados


def registrar_trade(entry, stop, tps, result, pnl, setup):
    os.makedirs("logs", exist_ok=True)
    linha = {
        "timestamp": datetime.utcnow().isoformat(),
        "entry": entry,
        "stop": stop,
        "tps": tps,
        "result": result,  # win/loss
        "pnl": pnl,
        "setup": setup
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(linha) + "\n")


# Retorna os últimos N trades


def carregar_trades():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        return [json.loads(l) for l in linhas[-MAX_JANELA:]]


# Ajusta comportamento com base em vitórias/derrotas


def ajustar_setup():
    historico = carregar_trades()
    if len(historico) < 5:
        return {"status": "skip", "reason": "poucos dados"}

    setups = {}
    for t in historico:
        s = t["setup"]
        if s not in setups:
            setups[s] = {"wins": 0, "losses": 0}
        if t["result"] == "win":
            setups[s]["wins"] += 1
        else:
            setups[s]["losses"] += 1

    relatorio = []
    for s, r in setups.items():
        total = r["wins"] + r["losses"]
        winrate = r["wins"] / total
        status = "mantido"
        if winrate < 0.4:
            status = "desativar"
        elif winrate > 0.7:
            status = "priorizar"
        relatorio.append({
            "setup": s,
            "winrate": round(winrate, 2),
            "acao": status
        })

    print("📊 Ajuste dinâmico de setups:", relatorio)
    return relatorio
