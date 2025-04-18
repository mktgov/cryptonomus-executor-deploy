def gerar_analise_suprema(dados):
    insights = []

    if abs(dados["funding_rate"]) > 0.05:
        insights.append("⚠️ Funding extremo detectado")

    if dados["oi_change"] > 10:
        insights.append("💥 Open Interest explodindo")

    if dados["heatmap_zone"] == "acima":
        insights.append("🔺 Liquidez acima = possível rompimento")
    elif dados["heatmap_zone"] == "abaixo":
        insights.append("🔻 Liquidez abaixo = armadilha")

    if dados["volatilidade"] < 1.2:
        insights.append("🧨 Volatilidade comprimida — breakout iminente")

    if dados["sentimento_social"] == "fomo":
        insights.append("😨 Otimismo excessivo — risco de queda")
    elif dados["sentimento_social"] == "medo":
        insights.append("🩸 Medo dominante — LONG oportuno")

    return {
        "ativo": dados["symbol"],
        "insights": insights,
        "direcao_sugerida": "buy" if dados["funding_rate"] < 0 else "sell",
        "probabilidade": "Alta" if len(insights) >= 4 else "Média",
        "tempo_estimado": "4h–12h"
    }
