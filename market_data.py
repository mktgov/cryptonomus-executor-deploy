# omega_executor/market_data.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

COINGLASS_API_KEY = os.getenv("COINGLASS_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

headers_coinglass = {
    "accept": "application/json",
    "coinglassSecret": COINGLASS_API_KEY
}
headers_cmc = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
}


def get_funding_rate_binance(symbol="BTCUSDT"):
    try:
        url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
        res = requests.get(url)
        data = res.json()
        return float(data[0]['fundingRate'])
    except Exception as e:
        print("[❌] Erro funding Binance:", str(e))
        return None


def get_open_interest_coinglass(symbol="BTC"):
    try:
        url = f"https://open-api.coinglass.com/public/v2/open_interest/chart?symbol={symbol}&interval=1h"
        res = requests.get(url, headers=headers_coinglass)
        data = res.json()
        return data['data'][-1]['sumOpenInterest']
    except Exception as e:
        print("[❌] Erro Open Interest Coinglass:", str(e))
        return None


def get_spot_vs_derivatives_coinglass(symbol="BTC"):
    try:
        url = f"https://open-api.coinglass.com/public/v2/future/longShortChart?symbol={symbol}&interval=1h"
        res = requests.get(url, headers=headers_coinglass)
        data = res.json()
        return data['data'][-1]  # Último ponto
    except Exception as e:
        print("[❌] Erro Volume Spot vs Derivatives:", str(e))
        return None


def get_btc_dominance_cmc():
    try:
        url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
        res = requests.get(url, headers=headers_cmc)
        data = res.json()
        return data['data']['btc_dominance']
    except Exception as e:
        print("[❌] Erro Dominância BTC:", str(e))
        return None


def testar_fontes():
    print("Funding Binance:", get_funding_rate_binance())
    print("Open Interest:", get_open_interest_coinglass())
    print("Spot vs Deriv:", get_spot_vs_derivatives_coinglass())
    print("BTC Dominance:", get_btc_dominance_cmc())


if __name__ == "__main__":
    testar_fontes()
