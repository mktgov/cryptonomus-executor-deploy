import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(layout="wide", page_title="CRYPTONΩMUS Dashboard")

st.title("⚔️ CRIPTONΩMUS - SHADOW TERMINAL")
st.markdown("Monitoração em tempo real dos setups ativos e ROI por mutante.")

log_dir = "logs/shadow"


def parse_log(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    data = []
    for line in lines:
        try:
            data.append(json.loads(line.strip()))
        except:
            continue
    return pd.DataFrame(data)


if not os.path.exists(log_dir):
    st.error(f"❌ Pasta de logs não encontrada: `{log_dir}`")
    st.stop()

log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]

for log_file in sorted(log_files):
    df = parse_log(os.path.join(log_dir, log_file))
    if df.empty:
        continue

    st.subheader(f"📊 {log_file.replace('.log', '')}")
    st.dataframe(df.tail(10), use_container_width=True)

    roi = df["roi"].sum() if "roi" in df.columns else 0
    st.success(f"💰 ROI acumulado: **{roi:.2f}%**")
