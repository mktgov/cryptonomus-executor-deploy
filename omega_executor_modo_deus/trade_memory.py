import os
import json
from datetime import datetime

LOG_PATH = "logs/results.log"
MAX_TRADES = 30


def log_result(entry, stop, tps, result, pnl, signal, symbol):
    os.makedirs("logs", exist_ok=True)
    linha = {
        "timestamp": datetime.utcnow().isoformat(),
        "entry": entry,
        "stop": stop,
        "tps": tps,
        "result": result,
        "pnl": pnl,
        "signal": signal,
        "symbol": symbol
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(linha) + "\n")


def ajustar_estrategia():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        linhas = f.readlines()[-MAX_TRADES:]
    trades = [json.loads(l) for l in linhas]
    if len(trades) < 5:
        return
    win_rate = sum(1 for t in trades if t["result"] == "win") / len(trades)
    print(
        f"📊 Win rate atual: {round(win_rate*100, 2)}% ({len(trades)} trades)")
