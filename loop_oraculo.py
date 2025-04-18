# loop_oraculo.py 🧠🕯️

import os
import sys
import time
import schedule
from datetime import datetime

# ⚠️ Patch para garantir que o Python encontre a pasta omega_executor ao rodar da raiz
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'omega_executor')))

from omega_executor.oraculo_executor import executar_oraculo_e_disparar


def iniciar_ritual():
    print(f"\n🕯️ [{datetime.utcnow().isoformat()}] RITUAL INICIADO")
    try:
        executar_oraculo_e_disparar()
    except Exception as e:
        print(f"⚠️ Falha na execução do Oráculo: {e}")
        log_falha(str(e))


def log_falha(mensagem):
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/oraculo_loop.log", "a") as f:
            f.write(f"[{datetime.utcnow().isoformat()}] FALHA: {mensagem}\n")
    except:
        pass


# 🧠 Frequência configurável (exemplo: a cada 5 segundos)
schedule.every(5).seconds.do(iniciar_ritual)

print("👁️‍🗨️ ORÁCULO EM MODO DE VIGÍLIA... AGUARDANDO O PRÓXIMO CICLO")

while True:
    schedule.run_pending()
    time.sleep(1)
