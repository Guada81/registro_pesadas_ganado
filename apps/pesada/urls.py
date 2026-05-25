from django.urls import path
from apps.pesada.views import registrar_pesada_view, listado_pesadas, historial_animal

app_name = "pesada"

urlpatterns = [
    path("registrar/", registrar_pesada_view, name="registrar_pesada"),
    path("listado/", listado_pesadas, name="listado"),
    path("animal/<int:animal_id>/", historial_animal, name="historial_animal"),
]