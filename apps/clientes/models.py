from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    num_telefono = models.CharField(max_length=10)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Celular(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='celulares')
    imei = models.CharField(max_length=15, blank=True, null=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    clave_desbloqueo = models.CharField(max_length=20)
