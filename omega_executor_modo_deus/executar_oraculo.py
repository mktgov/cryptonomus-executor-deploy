# omega_executor/executar_oraculo.py

from .oraculo import analisar_mercado

if __name__ == "__main__":
    resultado = analisar_mercado()

    print("\n📊 PLANO DE EXECUÇÃO CRIPTONOMUS:\n")
    print(f"🔹 Ativo: {resultado['ativo']}")
    print(f"🔹 Direção: {resultado['direcao']}")
    print(f"🔹 Entrada Ideal: ${resultado['entrada']}")
    print(f"🔹 Stop: ${resultado['stop']}")
    print(f"🔹 Alvo: ${resultado['alvo']}")
    print(f"🔹 Probabilidade: {resultado['probabilidade']}%")

    print(f"\n📜 Justificativa:\n{resultado['justificativa']}\n")

    print("✅ SINAL GERADO:")
    for chave, valor in resultado.items():
        print(f"{chave.upper()}: {valor}")

    print("\n🔁 Reavalie em 4h. Caminhe com os tubarões.\n")
