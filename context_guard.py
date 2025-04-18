from datetime import datetime


def verificar_contexto_mercado():
    agora = datetime.utcnow()
    hora = agora.hour
    dia_semana = agora.weekday()

    # Bloqueia sinais fora do horário das 9h–17h UTC
    if hora < 9 or hora > 17:
        return False, "Fora do horário operacional ideal (9h–17h UTC)"

    # Evita segunda-feira de manhã
    if dia_semana == 0 and hora < 12:
        return False, "Segunda de manhã: mercado instável"

    return True, "Contexto de mercado favorável"
