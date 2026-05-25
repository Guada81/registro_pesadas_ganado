from django.db.models import Count
from apps.pesada.models import Pesada


def obtener_resumen_general():
    ultima_pesada = (
        Pesada.objects
        .select_related("animal", "usuario")
        .order_by("-fecha_hora")
        .first()
    )

    return {
        "total_pesadas": Pesada.objects.count(),
        "ultima_pesada": ultima_pesada,
    }

def obtener_pesadas_por_operador():
    return (
        Pesada.objects
        .values("usuario__username")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

def obtener_metricas_operador(usuario):
    return {
        "total_pesadas_usuario": (
            Pesada.objects.filter(usuario=usuario).count()
        ),
        "ultima_pesada_usuario": (
            Pesada.objects
            .filter(usuario=usuario)
            .select_related("animal")
            .order_by("-fecha_hora")
            .first()
        ),
    }