from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from apps.usuario.models import Rol


class LoginView(ObtainAuthToken):
    """
    Login para la app móvil. Extiende el login estándar de DRF para:
    - Rechazar usuarios con rol LECTOR (no tienen acceso a mobile).
    - Devolver username y rol junto con el token, para que la app
      pueda aplicar permisos locales sin una consulta extra.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['user']

        if usuario.rol.codigo == Rol.LECTOR:
            return Response(
                {"detail": "El rol Lector no tiene acceso a la aplicación móvil."},
                status=status.HTTP_403_FORBIDDEN,
            )

        token, _ = Token.objects.get_or_create(user=usuario)

        return Response({
            "token": token.key,
            "username": usuario.username,
            "rol": usuario.rol.codigo,
        })