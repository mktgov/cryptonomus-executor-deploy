# omega_executor/oraculo_executor.py

import os
import sys

# ⚠️ Patch para garantir import mesmo fora do pacote
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from omega_executor.oraculo_core import analisar_mercado
from omega_executor.setup_guard import carregar_setups_promovidos
...
