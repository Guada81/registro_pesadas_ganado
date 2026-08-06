from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.pesada.models import Pesada
from apps.pesada.api.serializers import PesadaSerializer


class PesadaViewSet(viewsets.ModelViewSet):
    """ViewSet para listar, crear, consultar, actualizar y eliminar pesadas."""
    queryset = Pesada.objects.all().order_by('-fecha_hora')
    serializer_class = PesadaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)