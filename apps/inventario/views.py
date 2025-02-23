from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import InventarioForm
from .models import Producto


@login_required()
def inventario(request):
    return render(request, 'inventario.html')


@login_required()
def inventario_registro(request):
    producto_id = request.GET.get('id', None)  # Captura el ID desde la URL

    if producto_id:
        producto = get_object_or_404(Producto, id=producto_id)  # Obtiene el producto existente
        instance = producto
    else:
        instance = None  # No hay producto, se creará uno nuevo

    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=instance)  # Usa la instancia existente o None
        if form.is_valid():
            form.save()
            return redirect('/home')  # Redirige tras guardar
    else:
        form = InventarioForm(instance=instance)  # Carga el formulario con o sin datos

    return render(request, 'inventario_form.html', {'form': form})


@login_required()
def buscar_producto(request):
    query = request.GET.get('q', '')
    try:
        productos = Producto.objects.filter(nombre__icontains=query, activo=True)
        data = list(productos.values('id', 'nombre', 'cantidad', 'costo', 'precio'))
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error al buscar productos: {e}")
        return JsonResponse({'error': 'Error al buscar productos'}, status=500)


@login_required()
def actualizar_cantidad_producto(request):
    product_id = request.POST.get('id')
    change = int(request.POST.get('change'))
    new_quantity = 0

    try:
        producto = Producto.objects.get(id=product_id)
        if producto.cantidad + change < 0:
            return JsonResponse({'success': False, 'error': 'No puede restar más de la cantidad disponible.'})
        producto.cantidad = max(0, producto.cantidad + change)  # Evita cantidades negativas
        producto.save()
        success = True
        new_quantity = producto.cantidad
    except Producto.DoesNotExist:
        success = False

    return JsonResponse({'success': success, 'new_quantity': new_quantity})


@login_required()
def eliminar_producto(request):
    product_id = request.POST.get('producto_id')

    try:
        producto = Producto.objects.get(id=product_id)
        producto.activo = False
        producto.save()
        success = True
    except Producto.DoesNotExist:
        success = False

    return JsonResponse({'success': success})


@login_required()
def inventario_editar(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('/inventario')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = InventarioForm(instance=producto)

    return render(request, 'inventario_modificar.html', {
        'form': form, 'producto': producto
    })
