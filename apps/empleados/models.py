from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    CARGO_CHOICES = (
        ('gerente', 'Gerente'),
        ('tecnico', 'Técnico'),
        ('asistente', 'Asistente'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    num_telefono = models.CharField(max_length=10, blank=True, null=True)
    rfc = models.CharField(max_length=13)
    cargo = models.CharField(max_length=25, choices=CARGO_CHOICES, default='tecnico')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

