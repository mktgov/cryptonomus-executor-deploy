# omega_executor/trade_logic.py

import os
import ccxt
from dotenv import load_dotenv

from omega_executor.utils import (validar_payload, calcular_quantidade,
                                  mockar_ordem, executar_ordem_real)
from omega_executor.sentiment_guard import validar_sentimento
from omega_executor.signal_guard import validar_estrategia_extra
from omega_executor.notifier import enviar_alerta
from omega_executor.setup_guard import registrar_execucao, setup_permitido, calcular_peso_confiança
from omega_executor.shadow_setups import executar_mutantes_shadow
from omega_executor.cycle_sensor import detectar_ciclo
from omega_executor.shadow_logger import logar_execucao_shadow
from omega_executor.trade_simulator import simular_resultado_execucao  # ✅ Simula lucro mock

load_dotenv()

# 🔧 Risco modular por ativo
ATIVOS_ESPECIAIS = {
    "BTC": {
        "risco_pct": 2.0,
        "tp_mult": 3.0
    },
    "ETH": {
        "risco_pct": 1.5,
        "tp_mult": 2.5
    },
    "SOL": {
        "risco_pct": 1.2,
        "tp_mult": 2.0
    },
    "INJ": {
        "risco_pct": 1.0,
        "tp_mult": 1.8
    },
}


def handle_trade(data):
    validar_payload(data)
    ciclo = detectar_ciclo()
    data['cycle_fase'] = ciclo['fase']

    # Emoção e Tática
    valido_emocional, motivo_emocional = validar_sentimento(data)
    if not valido_emocional:
        enviar_alerta(f"🚫 BLOQUEADO (Emocional): {motivo_emocional}")
        return {"status": "blocked", "reason": motivo_emocional}

    valido_tatico, motivo_tatico = validar_estrategia_extra(data)
    if not valido_tatico:
        enviar_alerta(f"❌ BLOQUEADO (Tático): {motivo_tatico}")
        return {"status": "blocked", "reason": motivo_tatico}

    if not setup_permitido(data['strategy']):
        enviar_alerta(f"🔒 BLOQUEADO - Setup inválido: {data['strategy']}")
        return {"status": "blocked", "reason": "setup inválido"}

    # Risco por ativo
    ativo_base = data['symbol'].split("/")[0]
    config_ativo = ATIVOS_ESPECIAIS.get(ativo_base, {
        "risco_pct": 1.0,
        "tp_mult": 2.0
    })
    saldo_total = float(os.getenv("SALDO_TOTAL_USD", 1000))
    risco_pct = config_ativo["risco_pct"]

    try:
        qty = calcular_quantidade(data, saldo_total, risco_pct)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    signal = data['signal'].lower()
    price = float(data['price'])

    MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

    if MOCK_MODE:
        mockar_ordem(data['symbol'], signal, price, qty)
        resultado_simulado, lucro_bruto = simular_resultado_execucao(data)

        registrar_execucao(setup_nome=data['strategy'],
                           resultado=resultado_simulado,
                           fase=ciclo['fase'],
                           roi=lucro_bruto)

        enviar_alerta(
            f"🧪 MOCK {resultado_simulado.upper()} :: {data['symbol']} {signal.upper()} {qty:.2f} @ ${price:.2f} | ROI: ${lucro_bruto:.2f}"
        )

        resultados_shadow = executar_mutantes_shadow(data, ciclo)
        for r in resultados_shadow:
            logar_execucao_shadow(r['setup'], r['fase'], r['resultado'],
                                  r['roi'])

        return {
            "status": "executed",
            "symbol": data['symbol'],
            "volume": qty,
            "mode": "mock",
            "strategy": data['strategy'],
            "resultado_simulado": resultado_simulado,
            "roi": lucro_bruto,
            "shadow": resultados_shadow
        }

    # ✅ Execução real via exchange
    try:
        ordem_real = executar_ordem_real(data['symbol'], signal, qty)
        enviar_alerta(
            f"✅ EXECUÇÃO REAL :: {data['symbol']} {signal.upper()} {qty:.2f} @ ${price:.2f}"
        )
        registrar_execucao(
            setup_nome=data['strategy'],
            resultado="win",
            fase=ciclo['fase'],
            roi=0)  # ROI real virá do controle externo ou tracking futuro
        return {"status": "executed_real", "order": ordem_real}
    except Exception as e:
        enviar_alerta(f"❌ FALHA EXEC REAL: {str(e)}")
        return {"status": "error", "message": str(e)}
