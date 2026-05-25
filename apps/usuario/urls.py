from django.urls import path
from apps.usuario import views

app_name = "usuario"

urlpatterns = [
    path(
        "configuracion/",
        views.editar_unidad_preferida,
        name="configuracion",
    ),
]
