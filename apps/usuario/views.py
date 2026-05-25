from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.usuario.forms import PreferenciaUnidadForm


@login_required
def editar_unidad_preferida(request):
    usuario = request.user

    if request.method == "POST":
        form = PreferenciaUnidadForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Preferencia de unidad guardada correctamente."
            )
            return redirect("dashboard")
    else:
        form = PreferenciaUnidadForm(instance=usuario)

    return render(
        request,
        "usuario/editar_unidad.html",
        {"form": form},
    )

