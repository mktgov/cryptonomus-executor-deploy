# omega_executor/shadow_mode.py

import json
import os
from datetime import datetime
from omega_executor.utils import calcular_quantidade, mockar_ordem, executar_ordem_real
from omega_executor.notifier import enviar_alerta

SHADOW_LOG = "logs/shadow_trigger.log"

def executar_shadow(data, saldo_total, risco_pct):
    try:
        price = float(data["price"])
        signal = data["signal"].lower()
        qty = calcular_quantidade(data, saldo_total, risco_pct)
        entry = float(data["entry"])
        stop = float(data["stop"])
        tp = float(data["tps"][0]) if data.get("tps") else entry + (entry - stop) * 2

        # Mock PnL
        if signal == "buy":
            resultado = "win" if price <= entry and tp <= price else "loss"
        else:
            resultado = "win" if price >= entry and tp >= price else "loss"

        pnl = abs(tp - entry) * qty if resultado == "win" else -abs(entry - stop) * qty

        # Log
        os.makedirs("logs", exist_ok=True)
        with open(SHADOW_LOG, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "symbol": data["symbol"],
                "strategy": data["strategy"],
                "result": resultado,
                "pnl": round(pnl, 2),
                "entry": entry,
                "stop": stop,
                "tp": tp,
                "qty": qty
            }) + "\n")

        print(f"🕶️ [SHADOW] Simulação -> {data['symbol']} | Result: {resultado.upper()} | PnL: {pnl}")

        # Alerta
        alerta = f"🕶️ *SHADOW MODE*
Ativo: `{data['symbol']}`\nEstratégia: `{data['strategy']}`\nSimulação: `{resultado.upper()}`\nPnL Simulado: `{pnl}`"
        enviar_alerta(alerta)

    except Exception as e:
        print(f"[❌] Shadow Mode falhou: {e}")
