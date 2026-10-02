from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.animal.models import Animal
from apps.animal.api.serializers import AnimalSerializer


class AnimalViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Solo lista animales, para la sincronización de bajada de la app móvil.
    Incluye inactivos: la app necesita saber cuáles se dieron de baja.
    Sin paginación: la lista es chica y cambia poco.
    """
    queryset = Animal.objects.order_by('id')
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None