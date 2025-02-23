from django.db import models
from django.utils import timezone

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fecha} - {self.total}"

class DetalleVenta(models.Model):
    PRODUCTO = 'Producto'
    REPARACION = 'Reparación'
    TIPOS = [ (PRODUCTO, 'Producto'), (REPARACION, 'Reparación'),]

    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    nombre_producto = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} - {self.nombre_producto} - {self.subtotal}"


"""
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)

    def calcular_total(self):
        total_productos = sum(detalle.subtotal for detalle in self.detalles.all())
        total_servicio = self.servicio.precio if self.servicio else 0
        self.total = total_productos + total_servicio
        self.save()

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.calcular_total()
"""