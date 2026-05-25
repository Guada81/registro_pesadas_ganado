from django import forms
from apps.animal.models import Animal
from decimal import Decimal


class PesadaForm(forms.Form):
    animal = forms.ModelChoiceField(
        queryset=Animal.objects.filter(activo=True),
        label="Animal"
    )
    peso = forms.DecimalField(
    min_value=Decimal("0.01"),
    max_digits=8,
    decimal_places=2,
    label="Peso"
    )
    unidad_medida = forms.ChoiceField(
        choices=(
            ("kg", "Kilogramos"),
            ("lb", "Libras"),
        ),
        label="Unidad de medida"
    )