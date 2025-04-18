# omega_executor/risk_engine.py

import os


def calcular_volume_dinamico(saldo, risco_pct, entrada, stop):
    """
    Calcula o volume ideal baseado no risco da operação.

    Args:
        saldo (float): valor total da banca em USD
        risco_pct (float): percentual de risco por trade (ex: 1.5)
        entrada (float | str): preço de entrada
        stop (float | str): preço de stop

    Returns:
        float: quantidade (volume) ideal para operação
    """
    try:
        entrada = float(str(entrada).replace("$", "").strip())
        stop = float(str(stop).replace("$", "").strip())
    except Exception:
        raise ValueError("Entrada e Stop devem ser valores numéricos válidos.")

    dist_stop = abs(entrada - stop)

    if dist_stop == 0:
        raise ValueError("Stop e entrada não podem ser iguais.")

    risco_total = saldo * (risco_pct / 100)
    qtd = round(risco_total / dist_stop, 3)

    return qtd
