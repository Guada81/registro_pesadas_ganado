from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.pesada.services_dashboard import (
    obtener_resumen_general,
    obtener_pesadas_por_operador,
    obtener_metricas_operador,
)

@login_required
def dashboard_view(request):
    rol = request.user.rol.codigo

    contexto = {
        "rol": rol,
        "es_admin": rol == "ADMIN",
        "es_operador": rol == "OPERADOR",
        "es_lector": rol == "LECTOR",
    }

    if rol in ("ADMIN", "LECTOR"):
        contexto.update(obtener_resumen_general())

    if rol == "ADMIN":
        contexto["pesadas_por_operador"] = obtener_pesadas_por_operador()

    if rol == "OPERADOR":
        contexto.update(obtener_metricas_operador(request.user))

    return render(request, "dashboard.html", contexto)

