import ccxt


def coletar_dados_ativos(lista_ativos):
    exchange = ccxt.bybit()
    exchange.load_markets()

    ativos_dados = []
    for symbol in lista_ativos:
        ticker = exchange.fetch_ticker(symbol)
        oi = 15  # MOCK: % mudança OI
        funding = -0.03  # MOCK: funding negativo
        heatmap = "acima"
        sentimento = "medo"

        volatilidade = round(
            (ticker['high'] - ticker['low']) / ticker['open'] * 100, 2)

        ativos_dados.append({
            "symbol": symbol,
            "oi_change": oi,
            "funding_rate": funding,
            "heatmap_zone": heatmap,
            "volume_24h": ticker['quoteVolume'],
            "volatilidade": volatilidade,
            "sentimento_social": sentimento
        })

    return ativos_dados
