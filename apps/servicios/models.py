from django.db import models
from apps.clientes.models import Cliente, Celular
from apps.empleados.models import Empleado
from django.utils import timezone


class Servicio(models.Model):
    ESTADO_CHOICES = (
        ('ingresado', 'Ingresado'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    celular = models.ForeignKey(Celular, on_delete=models.CASCADE, null=False)
    descripcion = models.TextField()
    cotizacion = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ingresado')
    pagado = models.BooleanField(default=False)
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo campo para el anticipo
    activo = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    @property
    def saldo_pendiente(self):
        return self.cotizacion - self.anticipo


class AccionesServicio(models.Model):
    ESTADO_CHOICES = (
        ('ingresado', 'Ingresado'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    foto_antes = models.ImageField(upload_to='fotos_antes/', null=True, blank=True)
    foto_despues = models.ImageField(upload_to='fotos_despues/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ingresado')
    activo = models.BooleanField(default=True)