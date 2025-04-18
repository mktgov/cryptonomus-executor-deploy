# omega_executor/sentiment_listener.py

import requests
import time
import os

FNG_API = "https://api.alternative.me/fng/"
SLEEP_SECONDS = 300  # 5 minutos entre atualizações

CACHE_PATH = "sentiment_cache.txt"


def fetch_fear_and_greed():
    try:
        response = requests.get(FNG_API)
        data = response.json()
        value = int(data['data'][0]['value'])
        return value
    except Exception as e:
        print("[ERRO] Falha ao obter Fear & Greed Index:", e)
        return None


def salvar_valor(valor):
    with open(CACHE_PATH, "w") as f:
        f.write(str(valor))


def ler_valor():
    if not os.path.exists(CACHE_PATH):
        return None
    with open(CACHE_PATH, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return None


def iniciar_monitoramento():
    print("🔁 Monitor de sentimento iniciado...")
    while True:
        valor = fetch_fear_and_greed()
        if valor is not None:
            salvar_valor(valor)
            print(f"🧠 Fear & Greed atualizado: {valor}")
        else:
            print("⚠️ Valor não atualizado.")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    iniciar_monitoramento()
