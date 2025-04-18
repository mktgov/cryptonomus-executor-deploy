# omega_executor/cycle_sensor.py

import random
from omega_executor.market_data import (get_funding_rate_binance,
                                        get_open_interest_coinglass,
                                        get_spot_vs_derivatives_coinglass,
                                        get_btc_dominance_cmc)


def detectar_ciclo():
    try:
        funding = get_funding_rate_binance()
        oi = get_open_interest_coinglass()
        volume_ratio = get_spot_vs_derivatives_coinglass()
        btc_dominance = get_btc_dominance_cmc()

        print("[📊] FUNDING RATE:", funding)
        print("[📊] OPEN INTEREST:", oi)
        print("[📊] SPOT/DERIVATIVOS:", volume_ratio)
        print("[📊] DOMINÂNCIA BTC:", btc_dominance)

        fase = "lateral"
        risco = 1.0
        setups = ["Break + Retest"]
        modo = "neutro"

        if funding > 0.01 and volume_ratio < 0.9 and btc_dominance > 50:
            fase = "alta"
            risco = 2.0
            setups = ["Golden Cross Explosivo", "Institucional Volume Spike"]
            modo = "swing com pullback"
        elif funding < -0.01 and volume_ratio > 1.1 and btc_dominance < 47:
            fase = "queda"
            risco = 0.8
            setups = ["Capitulação RSI", "Reversão Suporte Major"]
            modo = "scalp reativo"

        return {
            "fase": fase,
            "risco_recomendado": risco,
            "modo": modo,
            "setup_ativo": setups,
            "dados": {
                "funding_rate": funding,
                "open_interest": oi,
                "volume_ratio": volume_ratio,
                "btc_dominance": btc_dominance
            }
        }

    except Exception as e:
        print("[⚠️] Erro ao detectar ciclo:", str(e))
        return {
            "fase": "desconhecido",
            "risco_recomendado": 1.0,
            "modo": "neutro",
            "setup_ativo": ["Break + Retest"],
            "dados": {}
        }


if __name__ == "__main__":
    print("[🔮] VISÃO CÓSMICA ATIVADA")
    contexto = detectar_ciclo()
    for k, v in contexto.items():
        print(f"{k.upper()}: {v}")
