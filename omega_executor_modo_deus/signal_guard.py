import os
import requests


def get_funding_rate(symbol="BTCUSDT"):
    try:
        res = requests.get(
            f"https://api.coinglass.com/public/v2/funding?symbol={symbol}")
        data = res.json()

        rate = float(data["data"][symbol]["binance"]["fundingRate"])
        print(f"💸 Funding Rate: {rate}")
        return rate
    except Exception as e:
        print("⚠️ Erro ao obter funding rate:", str(e))
        return None


def detectar_volume_anomalo(symbol="BTC"):
    try:
        res = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}")
        data = res.json()
        volume = float(data["market_data"]["total_volume"]["usd"])
        marketcap = float(data["market_data"]["market_cap"]["usd"])
        razao = volume / marketcap

        print(f"📊 Volume/MarketCap: {round(razao, 4)}")

        if razao > 0.25:
            return True, "Volume anômalo detectado"
        return False, "Volume dentro do padrão"

    except Exception as e:
        print("⚠️ Erro ao verificar volume:", str(e))
        return False, "Erro ao validar volume"


def validar_estrategia_extra(data):
    """
    Valida se condições de sentimento + dados on-chain permitem continuar.
    """
    if os.getenv("SIGNAL_GUARD", "false").lower() != "true":
        return True, "Signal Guard desativado"

    symbol = data.get("symbol", "BTCUSDT").replace("USDT", "")
    funding = get_funding_rate(symbol)
    volume_ok, motivo_volume = detectar_volume_anomalo(symbol)

    if funding is not None and funding > 0.08:
        return False, f"Funding rate elevado ({funding})"

    if not volume_ok:
        return False, motivo_volume

    return True, "Sinal aprovado pelas camadas avançadas"
