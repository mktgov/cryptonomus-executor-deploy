# omega_executor/supervisor.py

import json
from datetime import datetime, timedelta
import os

LOG_PATH = "logs/results.log"


def gerar_resumo():
    if not os.path.exists(LOG_PATH):
        return "⚠️ Nenhum log encontrado."

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            linhas = [json.loads(l) for l in f.readlines() if l.strip()]
    except Exception as e:
        return f"❌ Erro ao ler log: {str(e)}"

    hoje = datetime.utcnow().date()
    ultimos = [
        l for l in linhas
        if datetime.fromisoformat(l["timestamp"]).date() == hoje
    ]

    if not ultimos:
        return "⚠️ Nenhuma ordem executada hoje."

    total = len(ultimos)
    wins = [t for t in ultimos if t.get("result") == "win"]
    losses = [t for t in ultimos if t.get("result") == "loss"]
    winrate = len(wins) / total if total else 0
    pnl_total = sum(t.get("pnl", 0) for t in ultimos)
    ultima_ordem = ultimos[-1]

    msg = (
        f"\n📊 *Resumo CRYPTONΩMUS (Hoje)*\n"
        f"🗓 Data: {hoje.isoformat()}\n"
        f"📦 Total de trades: {total}\n"
        f"✅ Vitórias: {len(wins)} | ❌ Derrotas: {len(losses)}\n"
        f"📈 Win Rate: {winrate:.0%}\n"
        f"💰 Lucro Total: {pnl_total:.2f}\n"
        f"🕒 Última Execução: {ultima_ordem['entry']} @ {ultima_ordem['timestamp']}\n"
    )

    return msg


if __name__ == "__main__":
    print(gerar_resumo())
