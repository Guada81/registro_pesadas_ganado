from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()

KG_A_LB = Decimal("2.20462")


@register.filter
def mostrar_peso(peso_kg, unidad_destino="kg"):
    """
    Convierte un peso en kg a la unidad destino solo a nivel visual.
    """
    if peso_kg is None:
        return None

    peso_kg = Decimal(peso_kg)

    if unidad_destino == "lb":
        peso = peso_kg * KG_A_LB
    else:
        peso = peso_kg

    return peso.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
