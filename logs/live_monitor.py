import time
import os
import json

LOG_FILE = "logs/execution.log"


def monitorar():
    print("📡 Monitoramento em tempo real iniciado...\n")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)  # Vai para o final do arquivo

        while True:
            linha = f.readline()
            if not linha:
                time.sleep(1)
                continue
            try:
                data = json.loads(linha.strip())
                print(
                    f"\n🔄 Nova Execução: {data['symbol']} | {data['signal'].upper()} | {data['price']} @ {data['volume']}"
                )
            except Exception as e:
                print("⚠️ Erro ao processar linha:", linha, "\n", str(e))


if __name__ == "__main__":
    monitorar()
