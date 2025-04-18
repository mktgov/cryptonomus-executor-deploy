#!/bin/bash

echo "⚙️  Iniciando ativação visual do CRIPTONΩMUS..."
echo "🧹 Limpando instâncias antigas..."
pkill -f streamlit
pkill -f ngrok
sleep 1

# Inicia o Streamlit na porta 8501 em background
echo "🚀 Lançando dashboard Streamlit..."
nohup streamlit run omega_executor/dashboard_terminal.py --server.port=8501 > logs/streamlit.out 2>&1 &
sleep 8

# Verifica se o Streamlit está de pé antes de prosseguir
until curl -s http://localhost:8501; do
  echo "⏳ Aguardando Streamlit subir..."
  sleep 2
done

# Sobe túnel Ngrok
echo "🌐 Abrindo túnel Ngrok..."
nohup ./ngrok http 8501 > logs/ngrok.out 2>&1 &
sleep 4

# Captura URL
echo "🔍 URL pública gerada pelo Ngrok:"
curl --silent http://127.0.0.1:4040/api/tunnels | grep -o 'https://[0-9a-zA-Z.-]*\.ngrok-free\.app' | head -n 1

echo "✅ CRIPTONΩMUS Visual pronto. Acesse via URL acima."
