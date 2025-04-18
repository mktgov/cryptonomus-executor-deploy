import streamlit as st
import pandas as pd
import json
import os
import math
from datetime import datetime

st.set_page_config(page_title="CRIPTONΩMUS Dashboard", layout="wide")


# Utils
def carregar_logs(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(l) for l in f.readlines()]


def calcular_projecao_milhao(roi_medio, capital_inicial):
    capital = capital_inicial
    meses = 0
    while capital < 1_000_000:
        capital *= (1 + roi_medio / 100)
        meses += 1
        if meses > 240:  # 20 anos
            break
    return meses


# Load data
promoted = carregar_logs("logs/promoted_setups.json")
shadow = carregar_logs("logs/shadow_logs.json")
banidos = carregar_logs("logs/setups_banidos.log")
riscos = carregar_logs("logs/setups_em_risco.log")

# Layout
st.title("📈 CRIPTONΩMUS | Dashboard de Lucro e Seleção Natural")

# 1. Linha do Milhão
st.header("📈 Linha do Milhão (Projeção de ROI composto)")
roi_mock = sum([x.get("roi", 0)
                for x in shadow[-20:]]) / max(1, len(shadow[-20:]))
capital_inicial = 500
meses = calcular_projecao_milhao(roi_mock, capital_inicial)
st.metric("Projeção para R$1M",
          f"{meses} meses",
          help="Baseado em ROI médio das últimas execuções mock")

# 2. Setups Ativos
st.header("🔍 Setups Promovidos Ativos")
if isinstance(promoted, dict):
    ativos_df = pd.DataFrame.from_dict(promoted, orient="index")
    st.dataframe(ativos_df.style.format("{:.2f}"))
else:
    st.write("Nenhum setup promovido encontrado.")

# 3. Shadow Mode
st.header("🧬 Setups em Shadow Mode")
if shadow:
    df_shadow = pd.DataFrame(shadow)
    df_shadow = df_shadow.groupby("setup").agg({
        "roi": ["mean", "count"],
        "resultado":
        lambda x: (x == 'win').sum() / len(x) * 100
    }).reset_index()
    df_shadow.columns = ["Setup", "ROI Médio", "Trades", "Acurácia %"]
    st.dataframe(df_shadow)
else:
    st.write("Nenhum dado de Shadow Mode.")

# 4. Setups Banidos
st.header("💀 Setups Banidos")
if banidos:
    df_banidos = pd.DataFrame(banidos)
    st.dataframe(df_banidos)
else:
    st.write("Nenhum setup banido registrado.")

# 5. Alertas
st.header("⚠️ Setups em Risco")
if riscos:
    for r in riscos[-5:]:
        st.warning(f"{r['timestamp']} | {r['setup']} em risco: {r['motivo']}")
else:
    st.success("Nenhum setup em risco neste ciclo.")

st.markdown("---")
st.caption("Powered by CRIPTONΩMUS | OMNI")
