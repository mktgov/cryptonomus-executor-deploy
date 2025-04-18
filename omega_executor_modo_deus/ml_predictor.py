# omega_executor/ml_predictor.py

import random


def prever_direcao(data):
    """
    Simula uma previsão baseada em dados de entrada.
    Em um sistema real, conectaria a um modelo de IA (ex: sklearn, TensorFlow, etc).
    """
    # Exemplo simplificado: baseia direção no tempo atual ou no volume
    volume = float(data.get("volume", 0))
    signal = data.get("signal", "buy").lower()

    if volume > 50000:
        direcao = signal  # Confirma a direção proposta
        confianca = round(random.uniform(0.78, 0.95), 2)
    else:
        direcao = "buy" if signal == "sell" else "sell"  # Divergente
        confianca = round(random.uniform(0.55, 0.74), 2)

    print(f"🤖 Predição ML: {direcao.upper()} ({confianca * 100:.1f}%)")
    return direcao, confianca
