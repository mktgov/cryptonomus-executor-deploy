import os
import ccxt
import uuid
from dotenv import load_dotenv

load_dotenv()


def handle_trade(data):
    required_fields = [
        "symbol", "price", "volume", "time", "strategy", "signal", "source",
        "note"
    ]
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"Missing fields in payload: {', '.join(missing)}")

    print("\n📥 Webhook recebido:")
    for k, v in data.items():
        print(f"{k}: {v}")

    bybit_config = {
        'apiKey': os.getenv("BYBIT_API_KEY"),
        'secret': os.getenv("BYBIT_API_SECRET"),
        'enableRateLimit': True,
    }

    if os.getenv("BYBIT_TESTNET") == "true":
        bybit_config['options'] = {'defaultType': 'linear'}
        bybit_config['urls'] = {
            'api': {
                'public': 'https://api-testnet.bybit.com',
                'private': 'https://api-testnet.bybit.com',
            }
        }

    exchange = ccxt.bybit(bybit_config)
    exchange.load_markets()

    price = float(data["price"])
    volume = float(data["volume"])
    signal = data["signal"].lower()

    try:
        market = exchange.market(data["symbol"])
        symbol = market['symbol']
        qty = round(volume / price, 2)

        if signal in ["buy", "sell"]:
            # 🚨 MOCK ATIVADO
            order = {
                "id": str(uuid.uuid4()),
                "symbol": symbol,
                "side": signal,
                "price": price,
                "qty": qty,
                "status": "mocked"
            }
            print(f"🧪 MOCK -> Ordem simulada: {order}")
        else:
            raise ValueError("Signal must be 'buy' or 'sell'.")

        return {
            "status": "executed",
            "exchange": "bybit",
            "order_id": order['id'],
            "symbol": symbol,
            "price": price,
            "volume": qty,
            "mode": "mock"
        }

    except Exception as e:
        print("❌ Erro ao executar ordem:", str(e))
        return {"status": "error", "message": str(e)}
