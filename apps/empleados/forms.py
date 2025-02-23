from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from apps.empleados.models import Empleado

class EmpleadoForm(UserCreationForm):
    CARGO_CHOICES = [
        ('tecnico', 'Técnico'),
        ('asistente', 'Asistente'),
        ('gerente', 'Gerente'),
    ]

    nombre = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    num_telefono = forms.CharField(
        max_length=10,
        label='Número de Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Introduce un número de teléfono válido de 10 dígitos.'
            )
        ]
    )
    email = forms.EmailField(label='Correo', validators=[
        RegexValidator(
            regex=r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$',
            message='Introduce una dirección de correo válida.'
        )
    ])
    rfc = forms.CharField(
        max_length=13,
        label='RFC',
        validators=[
            RegexValidator(
                regex=r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$',
                message='Introduce un RFC válido.'
            )
        ]
    )
    cargo = forms.ChoiceField(choices=CARGO_CHOICES, label="Cargo")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'email': 'Correo',
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña'
        }
        help_texts = {
            'username': 'Hasta 150 caracteres. Letras, dígitos y @/./+/-/_ solamente.',
        }
        error_messages = {
            'username': {
                'invalid': 'Este nombre de usuario contiene caracteres inválidos.',
                'unique': 'Un usuario con este nombre ya existe.'
            },
            'email': {
                'invalid': 'Introduce una dirección de correo válida.'
            },
            'password1': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce una contraseña válida.',
            },
            'password2': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce una contraseña válida.',
                'password_mismatch': 'Las contraseñas no coinciden.'
            },
            'rfc': {
                'invalid': 'Introduce un RFC válido.',
            }
        }

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        for field in self.errors:
            self.fields[field].widget.attrs['class'] += ' is-invalid'
            self.fields[field].widget.attrs['class'] += ' error-message'

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            empleado, created = Empleado.objects.get_or_create(usuario=user)
            empleado.nombre = self.cleaned_data['nombre']
            empleado.apellidos = self.cleaned_data['apellidos']
            empleado.num_telefono = self.cleaned_data['num_telefono']
            empleado.rfc = self.cleaned_data['rfc']
            empleado.cargo = self.cleaned_data['cargo']
            empleado.save()
        return user


class EmpleadoUpdateForm(forms.ModelForm):
    CARGO_CHOICES = [
        ('tecnico', 'Técnico'),
        ('asistente', 'Asistente'),
        ('gerente', 'Gerente'),
    ]

    nombre = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    num_telefono = forms.CharField(
        max_length=10,
        label='Número de Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Introduce un número de teléfono válido de 10 dígitos.'
            )
        ]
    )
    email = forms.EmailField(label='Correo', validators=[
        RegexValidator(
            regex=r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$',
            message='Introduce una dirección de correo válida.'
        )
    ])
    rfc = forms.CharField(
        max_length=13,
        label='RFC',
        validators=[
            RegexValidator(
                regex=r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$',
                message='Introduce un RFC válido.'
            )
        ]
    )
    cargo = forms.ChoiceField(choices=CARGO_CHOICES, label="Cargo")

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellidos', 'num_telefono', 'email', 'rfc', 'cargo']

    def __init__(self, *args, **kwargs):
        super(EmpleadoUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        for field in self.errors:
            self.fields[field].widget.attrs['class'] += ' is-invalid'
            self.fields[field].widget.attrs['class'] += ' error-message'

    def save(self, commit=True):
        empleado = super().save(commit=False)
        usuario = empleado.usuario  # Asumiendo que hay un campo "usuario" en tu modelo Empleado

        # Actualiza los datos del usuario si se han modificado
        if self.cleaned_data['email'] != usuario.email:
            usuario.email = self.cleaned_data['email']
            usuario.save()

        if commit:
            empleado.save()
        return empleado


class PasswordChangeEmpleadoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']
        labels = {
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña'
        }
        error_messages = {
            'password1': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce una contraseña válida.',
            },
            'password2': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Introduce una contraseña válida.',
                'password_mismatch': 'Las contraseñas no coinciden.'
            }
        }

    def __init__(self, *args, **kwargs):
        super(PasswordChangeEmpleadoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        for field in self.errors:
            self.fields[field].widget.attrs['class'] += ' is-invalid'
            self.fields[field].widget.attrs['class'] += ' error-message'

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            empleado, created = Empleado.objects.get_or_create(usuario=user)
            empleado.save()
        return user