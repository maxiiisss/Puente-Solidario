from django.db import models
from django.utils import timezone

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo.capitalize()}: ${self.monto} - {self.descripcion}"