from django import forms
from apps.usuario.models import Usuario


class PreferenciaUnidadForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["unidad_medida_prefer"]
        labels = {
            "unidad_medida_prefer": "Unidad de medida preferida",
        }        
        
