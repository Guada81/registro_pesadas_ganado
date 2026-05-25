from django.contrib import admin
from .models import Pesada

@admin.register(Pesada)
class PesadaAdmin(admin.ModelAdmin):
    list_display = ("id", "animal", "peso", "unidad_medida", "fecha_hora")
    list_filter = ("unidad_medida", "fecha_hora")
