from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.usuario.models import Usuario, Rol


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("codigo", "activo")
    list_filter = ("activo",)
    search_fields = ("codigo",)
    ordering = ("codigo",)


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "rol",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "rol",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("username",)

    # Campos visibles al editar un usuario
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email")}),
        ("Rol y preferencias", {"fields": ("rol", "unidad_medida_prefer")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos al crear un usuario desde el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1",
                "password2",
                "rol",
                "unidad_medida_prefer",
                "is_active",
                "is_staff",
            ),
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["rol"].required = True
        return form