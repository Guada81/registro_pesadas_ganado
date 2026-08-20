from django.utils import timezone
from django.db import transaction
from django.db.models import Min, Max, Count, Avg
from django.contrib.auth import get_user_model

from apps.pesada.models import Pesada
from apps.pesada.utils import convertir_a_kg
from apps.animal.models import Animal
from apps.usuario.models import Rol

from decimal import Decimal

User = get_user_model()


class RegistroPesadaError(Exception):
    """Excepción de dominio para errores al registrar una pesada."""
    pass


@transaction.atomic
def registrar_pesada(
    *,
    animal_id: int = None,
    usuario: User, #marca una advertencia porque el get_user_model retorna una variable dinámica (se ejecuta en runtime)
    peso: Decimal,
    unidad_medida: str,
    fecha_hora=None,
    uuid_cliente=None,
    caravana_desconocida: str = None,
) -> Pesada: # Indica el tipo de dato, retorno de la función

    # 0. Idempotencia: si esta pesada ya fue registrada (mismo UUID de cliente),
    # devolver la existente en vez de crear una nueva ni fallar.
    if uuid_cliente is not None:
        pesada_existente = Pesada.objects.filter(uuid_cliente=uuid_cliente).first()
        if pesada_existente is not None:
            return pesada_existente
        
    # 1. Validar usuario
    if usuario is None or not usuario.is_authenticated:
        raise RegistroPesadaError("Usuario no autenticado.")

    # 2. Animal identificado o caravana desconocida
    animal = None
    if animal_id is not None:
        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            raise RegistroPesadaError("El animal no existe.")

        if not animal.activo:
            raise RegistroPesadaError("No se pueden registrar pesadas para un animal inactivo.")
        
    elif not caravana_desconocida:
        raise RegistroPesadaError("Debe indicar un animal o, si la caravana no fue reconocida, el número leído.")    

    # 3. Validar peso
    if peso is None or peso <= 0:
        raise RegistroPesadaError("El peso debe ser mayor a cero.")

    # 4. Fecha y hora
    if fecha_hora is None:
        fecha_hora = timezone.localtime()

    peso_kg = convertir_a_kg(peso, unidad_medida)    

    # 5. Crear la pesada
    pesada = Pesada.objects.create(
        animal=animal,
        usuario=usuario,
        peso=peso,
        peso_kg=peso_kg,
        unidad_medida=unidad_medida,
        fecha_hora=fecha_hora,
        uuid_cliente=uuid_cliente,
        caravana_desconocida=caravana_desconocida,
    )

    return pesada

@transaction.atomic
def invalidar_pesada(*, pesada_id: int, usuario: User) -> Pesada:
    """Marca una pesada como no válida (soft-delete). No se permite edición ni borrado físico."""

    if usuario is None or not usuario.is_authenticated:
        raise RegistroPesadaError("Usuario no autenticado.")

    try:
        pesada = Pesada.objects.get(id=pesada_id)
    except Pesada.DoesNotExist:
        raise RegistroPesadaError("La pesada no existe.")

    if usuario.rol.codigo == Rol.LECTOR:
        raise RegistroPesadaError("El rol Lector no tiene permisos para invalidar pesadas.")

    if usuario.rol.codigo == Rol.OPERADOR and pesada.usuario_id != usuario.id:
        raise RegistroPesadaError("Un operador solo puede invalidar sus propias pesadas.")

    if not pesada.valida:
        raise RegistroPesadaError("La pesada ya estaba invalidada.")

    pesada.valida = False
    pesada.save(update_fields=["valida"])

    return pesada

def obtener_metricas_animal(animal):
    pesadas = (
        Pesada.objects
        .filter(animal=animal, valida=True)
        .order_by("-fecha_hora")
    )

    metricas = pesadas.aggregate(
        total=Count("id"),
        peso_min=Min("peso_kg"),
        peso_max=Max("peso_kg"),
        peso_promedio=Avg("peso_kg"),
    )

    peso_min = metricas["peso_min"]
    peso_max = metricas["peso_max"]
    peso_promedio = metricas["peso_promedio"]

    if peso_min is not None:
        peso_min = peso_min.quantize(Decimal("0.01"))

    if peso_max is not None:
        peso_max = peso_max.quantize(Decimal("0.01"))

    if peso_promedio is not None:
        peso_promedio = peso_promedio.quantize(Decimal("0.01"))


    # Tendencia reciente (últimas dos pesadas)
    variacion_reciente = None
    tendencia_reciente = None

    ultimas_dos = list(pesadas[:2])

    if len(ultimas_dos) == 2:
        peso_ultima = ultimas_dos[0].peso_kg
        peso_anterior = ultimas_dos[1].peso_kg

        variacion_reciente = (peso_ultima - peso_anterior).quantize(Decimal("0.01"))

        if variacion_reciente > 0:
            tendencia_reciente = "up"
        elif variacion_reciente < 0:
            tendencia_reciente = "down"
        else:
            tendencia_reciente = "equal"

    return {
        "total_pesadas": metricas["total"],
        "peso_min": peso_min,
        "peso_max": peso_max,
        "peso_promedio": peso_promedio,
        "variacion_reciente": variacion_reciente,
        "tendencia_reciente": tendencia_reciente,
    }
