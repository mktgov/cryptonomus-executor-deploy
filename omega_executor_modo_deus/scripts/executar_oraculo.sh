#!/bin/bash

echo "🔁 Movendo para raiz do projeto..."
cd "$(dirname "$0")"

echo "📦 Executando oráculo via pacote (-m)..."
python3 -m omega_executor.oraculo_executor

echo "✅ Execução finalizada."
