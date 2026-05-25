from django import forms
from decimal import Decimal
from apps.animal.models import Animal
from apps.pesada.models import Pesada


class PesadaForm(forms.ModelForm):
    class Meta:
        model = Pesada
        fields = ["animal", "peso", "unidad_medida"]
        labels = {
            "animal": "Animal",
            "peso": "Peso",
            "unidad_medida": "Unidad de medida",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos para mostrar únicamente animales activos
        self.fields["animal"].queryset = Animal.objects.filter(activo=True)
        # Establecemos el valor mínimo de peso de forma dinámica y robusta
        self.fields["peso"].min_value = Decimal("0.01")