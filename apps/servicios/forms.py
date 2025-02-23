from django import forms
from .models import Servicio, Celular, Cliente, AccionesServicio
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe


class ServicioRegistroForm(forms.ModelForm):
    num_telefono = forms.CharField(max_length=10, required=True, label='Número de Teléfono')
    imei = forms.CharField(max_length=15, required=False, label='IMEI del Celular')
    marca = forms.CharField(max_length=100, required=True, label='Marca')
    modelo = forms.CharField(max_length=100, required=True, label='Modelo')
    clave_desbloqueo = forms.CharField(max_length=20, required=True, label='Clave de Desbloqueo')
    descripcion = forms.CharField(max_length=200, required=True, label='Descripción')
    cotizacion = forms.DecimalField(max_digits=10, required=True, decimal_places=2, label='Cotización')
    anticipo = forms.DecimalField(max_digits=10, required=True, decimal_places=2, label='Anticipo')  # Nuevo campo para el anticipo
    class Meta:
        model = Servicio
        fields = ['descripcion', 'cotizacion', 'anticipo']  # Añade el nuevo campo al formulario

    # Asumiendo que necesitas crear un nuevo Celular asociado en cada registro de Servicio
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            celular = Celular.objects.create(
                cliente=instance.cliente,
                imei=self.cleaned_data['imei'],
                marca=self.cleaned_data['marca'],
                modelo=self.cleaned_data['modelo'],
                clave_desbloqueo=self.cleaned_data['clave_desbloqueo']
            )
        return instance


class ServicioModificacionForm(forms.ModelForm):
    imei = forms.CharField(max_length=15, required=False, label='IMEI')
    marca = forms.CharField(max_length=100, required=False, label='Marca')
    modelo = forms.CharField(max_length=100, required=False, label='Modelo')
    clave_desbloqueo = forms.CharField(max_length=20, required=False, label='Clave desbloqueo')
    descripcion = forms.CharField(max_length=200, required=False, label='Descripción')

    class Meta:
        model = Servicio
        fields = ['descripcion', 'cotizacion', 'anticipo']

    def __init__(self, *args, **kwargs):
        super(ServicioModificacionForm, self).__init__(*args, **kwargs)
        
        if self.instance and hasattr(self.instance, 'cliente'):
            celular = self.instance.celular
            if celular:
                self.fields['imei'].initial = celular.imei
                self.fields['marca'].initial = celular.marca
                self.fields['modelo'].initial = celular.modelo
                self.fields['clave_desbloqueo'].initial = celular.clave_desbloqueo

        # Asegurar que todos los campos sean opcionales
        for field_name in self.fields:
            self.fields[field_name].required = False


class AccionesServicioForm(forms.ModelForm):
    estado_servicio = forms.ChoiceField(
        choices=Servicio.ESTADO_CHOICES,  # Asumiendo que tienes definido ESTADO_CHOICES en tu modelo Servicio
        label="Estado del Servicio",
        required=True
    )

    class Meta:
        model = AccionesServicio
        fields = ['estado_servicio', 'empleado', 'descripcion', 'costo', 'foto_antes', 'foto_despues']
        widgets = {
            'descripcion': forms.Textarea(attrs={'required': True}),  # Correctamente definido aquí
            'costo': forms.NumberInput(attrs={'required': True}),
            'foto_antes': forms.FileInput(attrs={'required': False}),
            'foto_despues': forms.FileInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super(AccionesServicioForm, self).__init__(*args, **kwargs)
        # Inicializar el campo estado_servicio con el valor actual si se está editando un objeto existente
        if self.instance and self.instance.pk:
            self.fields['estado_servicio'].initial = self.instance.Estado


class ModificacionAccionesServicioForm(forms.ModelForm):
    estado_servicio = forms.ChoiceField(
        choices=Servicio.ESTADO_CHOICES,
        label="Estado del Servicio",
        required=True
    )

    class Meta:
        model = AccionesServicio
        fields = ['estado_servicio', 'empleado', 'descripcion', 'costo', 'foto_antes', 'foto_despues']
        widgets = {
            'descripcion': forms.Textarea(attrs={'required': True}),
            'costo': forms.NumberInput(attrs={'required': True}),
            'foto_antes': forms.FileInput(attrs={'required': False}),  # Cambiado a False porque la subida no es obligatoria si ya existe un archivo
            'foto_despues': forms.FileInput(attrs={'required': False}),  # Ídem
        }

    def __init__(self, *args, **kwargs):
        super(ModificacionAccionesServicioForm, self).__init__(*args, **kwargs)
        # Inicializar los campos con los valores actuales si se está editando un objeto existente
        if self.instance and self.instance.pk:
            self.fields['estado_servicio'].initial = self.instance.servicio.estado
            self.fields['empleado'].initial = self.instance.empleado
            self.fields['descripcion'].initial = self.instance.descripcion
            self.fields['costo'].initial = self.instance.costo
            # Agregar enlaces para ver las fotos actuales, si existen
            if self.instance.foto_antes:
                self.fields['foto_antes'].widget = forms.FileInput(attrs={'required': False})
                self.fields['foto_antes'].help_text = mark_safe(f'<a href="{self.instance.foto_antes.url}" target="_blank">Ver foto actual</a>')
            if self.instance.foto_despues:
                self.fields['foto_despues'].widget = forms.FileInput(attrs={'required': False})
                self.fields['foto_despues'].help_text = mark_safe(f'<a href="{self.instance.foto_despues.url}" target="_blank">Ver foto actual</a>')