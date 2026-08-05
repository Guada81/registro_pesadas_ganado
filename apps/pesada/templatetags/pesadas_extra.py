from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()

# Usamos la misma constante oficial que en utils.py para garantizar simetría
LB_A_KG = Decimal("0.45359237")


@register.filter
def mostrar_peso(peso_kg, unidad_destino="kg"):
    """
    Convierte un peso en kg a la unidad destino solo a nivel visual.
    """
    if peso_kg is None:
        return None

    peso_kg = Decimal(str(peso_kg))

    if unidad_destino == "lb":
        # Al dividir por la misma constante, la reconversión es exacta
        peso = peso_kg / LB_A_KG
    else:
        peso = peso_kg

    return peso.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
