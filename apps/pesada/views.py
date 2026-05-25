from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from datetime import datetime, time

from apps.usuario.models import Rol
from apps.core.decorators import roles_permitidos

from apps.pesada.models import Pesada
from apps.pesada.forms import PesadaForm
from apps.pesada.services import registrar_pesada, RegistroPesadaError, obtener_metricas_animal

from apps.animal.models import Animal

@login_required
@roles_permitidos(Rol.ADMIN, Rol.OPERADOR)
def registrar_pesada_view(request):
    if request.method == "POST":
        form = PesadaForm(request.POST)
        if form.is_valid():
            try:
                registrar_pesada(
                    animal_id=form.cleaned_data["animal"].id,
                    usuario=request.user,
                    peso=form.cleaned_data["peso"],
                    unidad_medida=form.cleaned_data["unidad_medida"],
                )
                messages.success(request, "Pesada registrada correctamente.")
                return redirect("pesada:listado")
            except RegistroPesadaError as e:
                messages.error(request, str(e))
    else:
        form = PesadaForm(initial={"unidad_medida": request.user.unidad_medida_prefer})

    return render(request, "pesada/registrar_pesada.html", {"form": form})


@login_required
@roles_permitidos(Rol.ADMIN, Rol.OPERADOR, Rol.LECTOR)
def listado_pesadas(request):

    animal_id = request.GET.get("animal")
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")

    pesadas = (
        Pesada.objects
        .select_related("animal", "usuario")
        .order_by("-fecha_hora")
    )

    if animal_id:
        pesadas = pesadas.filter(animal_id=animal_id)

    if fecha_desde:
        desde_dt = make_aware(
            datetime.combine(
                datetime.strptime(fecha_desde, "%Y-%m-%d"),
                time.min
            )
        )
        pesadas = pesadas.filter(fecha_hora__gte=desde_dt)

    if fecha_hasta:
        hasta_dt = make_aware(
            datetime.combine(
                datetime.strptime(fecha_hasta, "%Y-%m-%d"),
                time.max
            )
        )
        pesadas = pesadas.filter(fecha_hora__lte=hasta_dt)

    animales = Animal.objects.all().order_by("id")

    # Paginación (15 pesadas por página)
    paginator = Paginator(pesadas, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Conservar otros parámetros de filtro al cambiar de página
    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    query_string = query_params.urlencode()

    return render(
        request,
        "pesada/listado_pesadas.html",
        {
            "pesadas": page_obj,
            "animales": animales,
            "animal_seleccionado": animal_id,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "query_string": query_string,
        },
    )

@login_required
@roles_permitidos(Rol.ADMIN, Rol.OPERADOR, Rol.LECTOR)
def historial_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    pesadas = (
        Pesada.objects
        .filter(animal=animal)
        .select_related("usuario")
        .order_by("-fecha_hora")
    )

    metricas = obtener_metricas_animal(animal)

    return render(
        request,
        "pesada/historial_animal.html",
        {
            "animal": animal,
            "pesadas": pesadas,
            **metricas,
        }
    )