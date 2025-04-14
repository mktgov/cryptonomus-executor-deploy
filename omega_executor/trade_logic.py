import os
import ccxt
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
        market = exchange.market(data["symbol"])  # Ex: SOL/USDT
        symbol = market['symbol']

        # Ajuste de volume para contratos perpétuos: arredondar para 2 casas
        qty = round(volume / price, 2)

        if signal == "buy":
            order = exchange.create_market_buy_order(symbol, qty)
        elif signal == "sell":
            order = exchange.create_market_sell_order(symbol, qty)
        else:
            raise ValueError("Signal must be 'buy' or 'sell'.")

        print(
            f"✅ Ordem enviada: {order['id']} ({signal.upper()} {qty} {symbol})"
        )
        print("📦 Resposta da Bybit:", order)

        return {
            "status": "executed",
            "exchange": "bybit",
            "order_id": order['id'],
            "symbol": symbol,
            "price": price,
            "volume": qty,
            "mode":
            "testnet" if os.getenv("BYBIT_TESTNET") == "true" else "live"
        }

    except Exception as e:
        print("❌ Erro ao executar ordem:", str(e))
        return {"status": "error", "message": str(e)}
