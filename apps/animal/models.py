from django.db import models

class Animal(models.Model):

    SEXOS = (
        ("M", "Macho"),
        ("H", "Hembra"),
    )

    nro_identificacion = models.CharField(max_length=50, unique=True)
    lote = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    raza = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXOS)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Animal {self.nro_identificacion}"