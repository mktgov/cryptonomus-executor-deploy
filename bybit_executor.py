import os
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
base_url = os.getenv("BYBIT_BASE_URL")

# Sessão de teste na Bybit (Testnet)
session = HTTP(api_key=api_key, api_secret=api_secret, testnet=True)


def executar_ordem(symbol, side, qty, price=None):
    try:
        ordem = session.place_order(
            category="linear",
            symbol=symbol,
            side=side.capitalize(),  # "Buy" ou "Sell"
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel")
        print("[✓] Ordem executada com sucesso:", ordem)
        return ordem
    except Exception as e:
        print("[X] Erro ao executar ordem:", e)
        return None
