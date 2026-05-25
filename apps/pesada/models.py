from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.pesada.utils import convertir_a_kg

class Pesada(models.Model):

    UNIDADES = (
        ('kg', 'Kilogramos'),
        ('lb', 'Libras'),
    )
    
    animal = models.ForeignKey("animal.Animal", on_delete=models.PROTECT, related_name='pesadas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField(default=timezone.now, db_index=True)
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES)
    peso_kg = models.DecimalField(max_digits=8, decimal_places=2, editable=False, null=False)
    valida = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.peso_kg is None:
            self.peso_kg = convertir_a_kg(self.peso, self.unidad_medida)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pesada: {self.peso}{self.unidad_medida} - {self.animal}"
