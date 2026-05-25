from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        from apps.usuario.models import Rol

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if "rol" not in extra_fields:
            rol, _ = Rol.objects.get_or_create(
                codigo=Rol.ADMIN,
                defaults={
                    "descripcion": "Administrador con acceso total a todas las funciones y configuraciones.",
                    "activo": True
                }
            )
            extra_fields["rol"] = rol

        return super().create_superuser(username, email, password, **extra_fields)

class Rol(models.Model):
    ADMIN = "ADMIN"
    OPERADOR = "OPERADOR"
    LECTOR = "LECTOR"

    ROLES_CODIGOS = (
        (ADMIN, "Administrador"),
        (OPERADOR, "Operador"),
        (LECTOR, "Lector"),
    )

    codigo = models.CharField(
        max_length=20,
        choices=ROLES_CODIGOS,
        unique=True
    )

    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.get_codigo_display()


class Usuario(AbstractUser):

    UNIDAD_KG = "kg"
    UNIDAD_LB = "lb"

    UNIDADES_PESO = (
        (UNIDAD_KG, "Kilogramos"),
        (UNIDAD_LB, "Libras"),
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="usuarios"
    )

    unidad_medida_prefer = models.CharField(
        max_length=10,
        choices=UNIDADES_PESO,
        default=UNIDAD_KG,
    )

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.username} ({self.rol.codigo})"    
