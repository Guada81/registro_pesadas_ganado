from django.core.exceptions import PermissionDenied
from functools import wraps


def roles_permitidos(*codigos_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                raise PermissionDenied

            if user.rol.codigo not in codigos_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
