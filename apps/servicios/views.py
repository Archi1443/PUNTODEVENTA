from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.servicios.models import Servicio, AccionesServicio
from apps.clientes.models import Cliente, Celular
from techsolutionswebsite import settings
from django.contrib import messages
from .forms import ServicioRegistroForm, ServicioModificacionForm, AccionesServicioForm, ModificacionAccionesServicioForm
from django.forms import inlineformset_factory
from .models import Servicio, AccionesServicio
from django.forms import BaseInlineFormSet
from django.core.mail import send_mail
from django.conf import settings
from apps.utils import enviar_correo
from apps.clientes.forms import ClienteForm
from django.db.models import Q

@login_required
def verificar_cliente(request):
    num_telefono = request.GET.get('num_telefono')
    cliente = Cliente.objects.filter(num_telefono=num_telefono).first()
    
    if cliente:
        nombre_completo = f"{cliente.nombre} {cliente.apellidos}"
        return JsonResponse({'existe': True, 'nombre_completo': nombre_completo})
    else:
        return JsonResponse({'existe': False})

@login_required
def filtrar_servicios(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', 'todos')
    if query:
        if estado == 'todos':
            servicios = Servicio.objects.filter(
                Q(id__icontains=query,) | Q(cliente__nombre__icontains=query),
                activo=True
            ).select_related('celular', 'cliente')
        else:
            servicios = Servicio.objects.filter(
                Q(id__icontains=query,) | Q(cliente__nombre__icontains=query),
                estado=estado,
                activo=True
            ).select_related('celular', 'cliente')
    else:
        if estado == 'todos':
            servicios = Servicio.objects.filter(activo=True).select_related('celular', 'cliente')
        else:
            servicios = Servicio.objects.filter(estado=estado, activo=True).select_related('celular', 'cliente')
    data = []
    for servicio in servicios:
        data.append({
            'id': servicio.id,
            'estado': servicio.estado,
            'descripcion': servicio.descripcion,
            'celular_imei': servicio.celular.imei,
            'celular_marca': servicio.celular.marca,
            'celular_modelo': servicio.celular.modelo,
            'cliente': f"{servicio.cliente.nombre} {servicio.cliente.apellidos}",
        })
    
    return JsonResponse(data, safe=False)



@login_required()
def servicios_clientes_registro(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.activo = True  # Establecer activo como True
            cliente.save()
            return redirect('/home')
    else:
        form = ClienteForm()
    return render(request, 'servicios_clientes_form.html', {
        'form': form
    })


@login_required
def eliminar_servicio(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio_id')
        servicio = get_object_or_404(Servicio, id=servicio_id)
        try:
            servicio.activo = False
            servicio.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def servicios_editar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    celular_actual = servicio.celular  # Guardar el celular actual antes de cualquier cambio

    if request.method == 'POST':
        form = ServicioModificacionForm(request.POST, instance=servicio)
        if form.is_valid():
            nuevo_imei = form.cleaned_data['imei']
            if nuevo_imei:
                celular, created = Celular.objects.get_or_create(
                    cliente=servicio.cliente,
                    imei=nuevo_imei,
                    defaults={
                        'marca': form.cleaned_data['marca'],
                        'modelo': form.cleaned_data['modelo'],
                        'clave_desbloqueo': form.cleaned_data['clave_desbloqueo'],
                    }
                )
            else:
                messages.error(request, 'El IMEI no puede estar vacío.')
                return render(request, 'servicios_modificar.html', {'form': form})

            # Crear o actualizar el nuevo Celular
            celular, created = Celular.objects.get_or_create(
                cliente=servicio.cliente,
                imei=nuevo_imei,
                defaults={
                    'marca': form.cleaned_data['marca'],
                    'modelo': form.cleaned_data['modelo'],
                    'clave_desbloqueo': form.cleaned_data['clave_desbloqueo'],
                }
            )
            if not created:
                # Si el celular ya existía y se encontró por el IMEI, actualizamos el resto de los datos.
                celular.cliente = servicio.cliente
                celular.marca = form.cleaned_data['marca']
                celular.modelo = form.cleaned_data['modelo']
                celular.clave_desbloqueo = form.cleaned_data['clave_desbloqueo']
                celular.save()

            # Asignar el nuevo celular al servicio y guardar el servicio
            servicio.celular = celular
            if servicio.anticipo < servicio.cotizacion:
                servicio.pagado = False
            servicio.save()
            messages.success(request, 'Servicio actualizado correctamente.')
            return redirect('servicios_gestion')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ServicioModificacionForm(instance=servicio)

    return render(request, 'servicios_modificar.html', {
        'form': form,
    })

@login_required()
def servicios_registro(request):
    if request.method == 'POST':
        form = ServicioRegistroForm(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente.objects.get(num_telefono=request.POST.get('num_telefono'))
            except Cliente.DoesNotExist:
                return render(request, 'servicios_form.html', {'form': form})
            
            celular, created = Celular.objects.get_or_create(
                cliente=cliente,
                imei=request.POST.get('imei'),
                defaults={
                    'marca': request.POST.get('marca'),
                    'modelo': request.POST.get('modelo'),
                    'clave_desbloqueo': request.POST.get('clave_desbloqueo')
                }
            )
            
            servicio = form.save(commit=False)
            if servicio.anticipo < servicio.cotizacion:
                servicio.pagado = False
            servicio.cliente = cliente
            servicio.celular = celular
            servicio.total = servicio.cotizacion
            servicio.save()
            
            # Crear una nueva acción asociada al servicio recién creado
            AccionesServicio.objects.create(
                servicio=servicio,
                empleado=None,
                descripcion="Se ingresó un dispositivo nuevo",
                estado="Ingresado",
                costo=0,
                foto_antes=None,
                foto_despues=None
            )
            
            return JsonResponse({'servicioId': servicio.id})
        else:
            print(form.errors)  
    else:
        form = ServicioRegistroForm()
    
    return render(request, 'servicios_form.html', {'form': form})


@login_required()
def servicios_consulta(request, id):
    try:
        servicio = Servicio.objects.get(id=id)
        acciones = AccionesServicio.objects.filter(servicio=servicio)
    except Servicio.DoesNotExist:
        return render(request, 'error.html', {'error': 'Servicio no encontrado'})
    return render(request, 'servicios_consulta.html', {
        'servicio': servicio,
        'cliente': servicio.cliente,
        'celular': servicio.celular,
        'acciones': acciones 
    })


@login_required()
def servicios_gestion(request):
    return render(request, 'servicios_gestion.html')


@login_required()
def servicios_acciones(request, id):
    try:
        servicio = Servicio.objects.get(id=id)
        acciones = AccionesServicio.objects.filter(servicio=servicio)
    except Servicio.DoesNotExist:
        return render(request, 'error.html', {'error': 'Servicio no encontrado'})
    return render(request, 'servicios_acciones.html', {
        'servicio': servicio,
        'cliente': servicio.cliente,
        'celular': servicio.celular,
        'acciones': acciones 
    })


@login_required()
def acciones_registro(request, id):
    servicio = get_object_or_404(Servicio, id=id)  # Obtener el objeto Servicio o devolver un error 404 si no existe

    if request.method == 'POST':
        form = AccionesServicioForm(request.POST, request.FILES)  # Asegúrate de manejar también request.FILES para los campos de archivo
        if form.is_valid():
            accion = form.save(commit=False)
            servicio.cotizacion = servicio.cotizacion
            servicio.estado = request.POST.get('estado_servicio')
            if servicio.anticipo < servicio.cotizacion:
                servicio.pagado = False
            servicio.total += accion.costo
            servicio.save()
            accion.servicio = servicio  # Asignar el servicio a la acción
            accion.estado = request.POST.get('estado_servicio')
            accion.save()
            return redirect('/home')  # Considera usar reverse_lazy para urls dinámicas
    else:
        form = AccionesServicioForm()

    return render(request, 'acciones_form.html', {
        'form': form,
        'servicio': servicio  # Pasar el servicio al template puede ser útil si quieres mostrar detalles en la página
    })

@login_required()
def eliminar_accion(request):
    accionId = request.POST.get('accion_id')
    servicioId = request.POST.get('servicio_id')

    try:
        accion = AccionesServicio.objects.get(id=accionId)
        accion.activo = False
        servicio = servicio = Servicio.objects.get(id=servicioId)
        servicio.total -= accion.costo
        servicio.save()
        accion.save()
        success = True
    except AccionesServicio.DoesNotExist:
        success = False

    return JsonResponse({'success': success})


@login_required
def acciones_editar(request, id):
    accion = get_object_or_404(AccionesServicio, id=id)
    servicio = accion.servicio  # Asumiendo que AccionesServicio tiene una relación con Servicio

    if request.method == 'POST':
        form = ModificacionAccionesServicioForm(request.POST, request.FILES, instance=accion)
        if form.is_valid():
            accion = form.save()

            # Actualiza el estado del servicio aquí
            servicio.estado = request.POST.get('estado_servicio')
            servicio.save()
            accion.servicio = servicio
            accion.estado = request.POST.get('estado_servicio')
            accion.save()

            messages.success(request, 'La acción de servicio ha sido actualizada exitosamente.')
            return redirect('alguna_url_para_redireccionar')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = ModificacionAccionesServicioForm(instance=accion)

    return render(request, 'acciones_modificar.html', {
        'form': form,
        'accion': accion
    })