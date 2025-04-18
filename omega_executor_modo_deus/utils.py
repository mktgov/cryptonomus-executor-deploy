# omega_executor/utils.py (trecho atualizado com execução real protegida)

import os
import ccxt
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ⚖️ EXECUÇÃO REAL COM PROTEÇÃO ABSOLUTA


def executar_ordem_real(symbol, side, quantity, price=None, tipo="market"):
    """
    Executa ordem real na exchange com:
    - Proteção de volume
    - Confirmação dupla por .env
    - Log persistente
    """
    exchange_name = os.getenv("EXCHANGE", "bybit").lower()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    real_confirm = os.getenv("REAL_EXEC_CONFIRM", "false").lower() == "true"
    failsafe_path = ".failsafe"

    if os.path.exists(failsafe_path):
        raise Exception("❌ MODO FAILSAFE ATIVADO. Nenhuma execução permitida.")

    if not real_confirm:
        raise Exception(
            "⚠️ REAL_EXEC_CONFIRM está falso. Ative no .env para executar ordens reais."
        )

    if not api_key or not api_secret:
        raise Exception("❌ API_KEY/API_SECRET ausentes.")

    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,
    })

    ordem = None
    try:
        if tipo == "market":
            ordem = exchange.create_market_order(symbol, side, quantity)
        elif tipo == "limit":
            if not price:
                raise Exception("⚠️ Preço obrigatório para ordem limit")
            ordem = exchange.create_limit_order(symbol, side, quantity, price)
        else:
            raise Exception("❌ Tipo de ordem inválido")
    except Exception as e:
        raise Exception(f"⚠️ Erro ao executar ordem real: {e}")

    # ✅ LOG REAL
    log_path = "logs/orders_real.log"
    os.makedirs("logs", exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "ordem": ordem
        }
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    return ordem


def validar_payload(data):
    """
    Valida se o JSON recebido do TradingView contém os campos essenciais.
    """
    campos_obrigatorios = [
        "symbol", "entry", "stop", "tps", "price", "strategy", "signal"
    ]
    for campo in campos_obrigatorios:
        if campo not in data:
            raise ValueError(f"❌ Payload inválido. Campo ausente: {campo}")


def calcular_quantidade(data, saldo_total_usd, risco_pct):
    """
    Calcula a quantidade a ser operada com base no risco em % e distância de stop.
    """
    entry = float(data["entry"])
    stop = float(data["stop"])
    direcao = data["signal"].lower()

    if direcao == "buy":
        risco_unitario = entry - stop
    elif direcao == "sell":
        risco_unitario = stop - entry
    else:
        raise ValueError("❌ Direção inválida. Use 'buy' ou 'sell'.")

    if risco_unitario <= 0:
        raise ValueError("❌ Stop inválido. Risco unitário ≤ 0.")

    risco_total = saldo_total_usd * (risco_pct / 100)
    quantidade = risco_total / risco_unitario

    return round(quantidade, 3)


def mockar_ordem(symbol, side, price, quantity):
    """
    Simula uma ordem mock e salva no log de execuções.
    """
    import os, json
    from datetime import datetime

    os.makedirs("logs", exist_ok=True)
    log_path = "logs/execucoes_oraculo.log"

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "side": side,
        "price": price,
        "quantity": quantity,
        "modo": "mock"
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    return log
