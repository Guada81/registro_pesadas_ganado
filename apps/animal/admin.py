from django.contrib import admin
from apps.animal.models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("id", "nro_identificacion", "activo")
    search_fields = ("nro_identificacion",)
    list_filter = ("activo",)

