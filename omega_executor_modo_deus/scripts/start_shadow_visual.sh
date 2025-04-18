#!/bin/bash

echo "🌑 Ativando Modo SHADOW VISUAL do CRIPTONΩMUS..."

# 1. Inicia dashboard visual na porta 8501
echo "📊 Ligando Dashboard..."
streamlit run omega_executor/dashboard_terminal.py --server.port=8501 &

sleep 5

# 2. Inicia Ngrok para expor o dashboard
echo "🌐 Iniciando Ngrok na porta 8501..."
./ngrok http 8501 &

sleep 5

# 3. Roda oráculo em loop shadow
echo "🔮 Executando Shadow Loop..."
python3 omega_executor/loop_oraculo.py
