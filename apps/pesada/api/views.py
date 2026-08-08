from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.pesada.models import Pesada
from apps.pesada.api.serializers import PesadaSerializer
from apps.pesada.services import invalidar_pesada, RegistroPesadaError


class PesadaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet para pesadas. Solo permite listar, ver detalle y crear.
    No se permite update ni delete: los registros son inmutables.
    Para corregir un error, usar la acción 'invalidar' y cargar una
    pesada nueva.
    """
    queryset = Pesada.objects.select_related('animal', 'usuario').order_by('-fecha_hora')
    serializer_class = PesadaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def invalidar(self, request, pk=None):
        try:
            pesada = invalidar_pesada(pesada_id=pk, usuario=request.user)
        except RegistroPesadaError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(pesada)
        return Response(serializer.data, status=status.HTTP_200_OK)