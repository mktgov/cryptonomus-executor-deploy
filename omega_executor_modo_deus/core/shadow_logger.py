# omega_executor/shadow_logger.py

import os
import json
from datetime import datetime


def logar_execucao_shadow(setup, fase, resultado, roi):
    os.makedirs("logs/shadow", exist_ok=True)
    caminho = f"logs/shadow/{setup.replace(' ', '_')}.log"

    registro = {
        "timestamp": datetime.utcnow().isoformat(),
        "setup": setup,
        "fase": fase,
        "resultado": resultado.lower(),
        "roi": round(roi, 3)
    }

    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
