
import random
from datetime import date, datetime

ZONA = "España"


def generar_precios(fecha: date, seed: int | None = None) -> list[tuple[datetime, float, str]]:
    """
    Genera 24 precios horarios simulados para una fecha.

    Simula el patrón real del mercado eléctrico: precios bajos de madrugada,
    pico por la mañana y pico mayor por la tarde-noche.

    Devuelve una lista de tuplas (fecha_hora, precio_eur_mwh, zona).
    """
    rng = random.Random(seed)
    precios = []

    for hora in range(24):
        # Precio base según la franja horaria
        if 0 <= hora < 7:        # Madrugada: valle
            base = 45.0
        elif 7 <= hora < 11:     # Mañana: pico
            base = 95.0
        elif 11 <= hora < 18:    # Mediodía: medio (solar)
            base = 70.0
        else:                    # Tarde-noche: pico máximo
            base = 110.0

        # Ruido aleatorio de ±15%
        precio = round(base * rng.uniform(0.85, 1.15), 2)
        fecha_hora = datetime(fecha.year, fecha.month, fecha.day, hora)
        precios.append((fecha_hora, precio, ZONA))

    return precios
