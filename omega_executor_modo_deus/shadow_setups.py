# omega_executor/shadow_setups.py

import random


def golden_cross_mutante_A(data):
    """
    Mutante A: Golden Cross com volume nas últimas 3 velas
    """
    try:
        ema_50 = data['ema_50']
        ema_200 = data['ema_200']
        volumes = data['volumes'][-3:]  # Lista com os 3 últimos candles
        media_volume = data['media_volume_20']
        rsi = data['rsi']

        cond_cross = ema_50 > ema_200
        cond_volume = sum(volumes) > (3 * media_volume)
        cond_rsi = rsi > 55

        ativo = cond_cross and cond_volume and cond_rsi
        return ativo

    except Exception as e:
        print(f"[⚠️] Erro Mutante A: {e}")
        return False


def golden_cross_mutante_B(data):
    """
    Mutante B: Golden Cross com funding rate mínimo de 0.015
    """
    try:
        ema_50 = data['ema_50']
        ema_200 = data['ema_200']
        funding_rate = data['funding_rate']
        rsi = data['rsi']

        cond_cross = ema_50 > ema_200
        cond_funding = funding_rate > 0.015
        cond_rsi = rsi > 55

        ativo = cond_cross and cond_funding and cond_rsi
        return ativo

    except Exception as e:
        print(f"[⚠️] Erro Mutante B: {e}")
        return False


# Mapa de mutações disponíveis
SETUPS_MUTANTES = {
    "GoldenCross_MutA": golden_cross_mutante_A,
    "GoldenCross_MutB": golden_cross_mutante_B,
}


def avaliar_mutantes(data):
    """
    Avalia todos os setups mutantes ativos com os dados fornecidos.
    Retorna lista de setups aprovados.
    """
    aprovados = []
    for nome, func in SETUPS_MUTANTES.items():
        if func(data):
            aprovados.append(nome)
    return aprovados
