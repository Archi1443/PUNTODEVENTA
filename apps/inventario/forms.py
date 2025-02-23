from django import forms
from .models import Producto


class InventarioForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, label="Nombre")
    cantidad = forms.IntegerField(label="Cantidad")
    costo = forms.DecimalField(max_digits=10, decimal_places=2, label="Costo")
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")

    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'costo', 'precio']
