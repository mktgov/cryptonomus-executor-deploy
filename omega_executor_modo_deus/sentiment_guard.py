# omega_executor/sentiment_guard.py

import os


# ✅ Lê o índice de medo e ganância salvo pelo listener
def ler_valor_fear_greed():
    try:
        with open("cache/fear_greed.json", "r") as f:
            import json
            data = json.load(f)
            return data["value"], data["classification"]
    except:
        return None, None


def validar_sentimento(data):
    """
    Verifica se o ambiente emocional de mercado permite a entrada
    """
    fear_greed_valor, classificacao = ler_valor_fear_greed()

    if fear_greed_valor is None:
        return True, "Índice indisponível (default liberado)"

    fg = int(fear_greed_valor)

    # 🚨 BLOQUEIA extremos
    if fg <= 20:
        return False, f"Mercado em PÂNICO (Fear & Greed: {fg})"
    if fg >= 80:
        return False, f"Mercado em EUFORIA (Fear & Greed: {fg})"

    return True, f"Aprovado (Fear & Greed: {fg} - {classificacao})"
