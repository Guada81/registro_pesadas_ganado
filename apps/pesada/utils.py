from decimal import Decimal, ROUND_HALF_UP

LB_A_KG = Decimal("0.45359237")

def convertir_a_kg(peso: Decimal, unidad: str) -> Decimal:
    """
    Convierte un peso a kilogramos.
    Devuelve siempre Decimal con 2 decimales.
    """
    if unidad == "kg":
        return peso.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if unidad == "lb":
        return (peso * LB_A_KG).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    raise ValueError(f"Unidad de medida no soportada: {unidad}")
