from venv import logger
from django.contrib.auth.decorators import login_required
import mercadopago
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from apps.servicios.models import Servicio, Cliente, AccionesServicio
from apps.inventario.models import Producto
from .models import Venta, DetalleVenta
import mercadopago
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Venta, DetalleVenta
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Venta, DetalleVenta
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Venta, DetalleVenta
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from collections import defaultdict
from .models import Venta, DetalleVenta
from collections import Counter

def generar_reporte_ventas(request):
    # Obtener las fechas de los parámetros GET
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Si no se proporcionan fechas, usar la última semana como rango por defecto
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        today = datetime.now().date()
        start_date = today - timedelta(days=7)
        end_date = today

    # Obtener las ventas en el rango de fechas
    ventas_ultima_semana = Venta.objects.filter(fecha__date__gte=start_date, fecha__date__lte=end_date)

    # Preparar datos para el reporte
    ventas = []
    for detalle in DetalleVenta.objects.filter(venta__in=ventas_ultima_semana):
        ventas.append({
            "fecha": detalle.fecha.strftime('%Y-%m-%d'),
            "nombre_producto": detalle.nombre_producto,
            "cantidad": detalle.cantidad,
            "precio": detalle.precio_unitario,
            "costo": detalle.costo
        })

    # Contar los productos vendidos
    product_counter = Counter()
    for venta in ventas:
        product_counter[venta["nombre_producto"]] += venta["cantidad"]

    # Obtener el producto más vendido
    most_sold_product = product_counter.most_common(1)[0] if product_counter else ("N/A", 0)

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Título del reporte
    titulo = Paragraph("Reporte de Productos Vendidos - Tech Solutions", styles['Title'])
    story.append(titulo)
    story.append(Spacer(1, 12))

    # Fechas del reporte
    subtitulo = Paragraph(f"Desde: {start_date_str} Hasta: {end_date_str}", styles['Heading2'])
    story.append(subtitulo)
    story.append(Spacer(1, 12))

    # Producto más vendido
    producto_mas_vendido = Paragraph(f"Producto Más Vendido: {most_sold_product[0]} (Cantidad: {most_sold_product[1]})", styles['Heading2'])
    story.append(producto_mas_vendido)
    story.append(Spacer(1, 12))

    # Filtrar y resumir ventas
    resumen_ventas = defaultdict(lambda: {'cantidad_total': 0, 'ganancia_total': 0, 'costo_total': 0, 'venta_total': 0})
    total_ganancia = 0  # Inicializar total de ganancia
    total_costo = 0
    total_venta = 0
    for venta in ventas:
        costo = venta['costo']
        
        producto = venta['nombre_producto']
        resumen_ventas[producto]['cantidad_total'] += venta['cantidad']
        ganancia_producto = (venta['cantidad'] * venta['precio']) - venta['costo']
        gananciatotal = (venta['cantidad'] * venta['precio'])
        
        resumen_ventas[producto]['ganancia_total'] += ganancia_producto
        resumen_ventas[producto]['venta_total'] += ganancia_producto
        total_ganancia += ganancia_producto  # Sumar a total de ganancia
        total_venta += gananciatotal
        resumen_ventas[producto]['costo_total'] += costo
        resumen_ventas[producto]['venta_total'] += costo
        total_costo += costo
        
    # Datos para la tabla
    data = [["Producto", "Cantidad Total", "Costo", "Venta", "Ganancia Total"]]
    for producto, datos in resumen_ventas.items():
        data.append([producto, datos['cantidad_total'], f"${datos['costo_total']}", f"${datos['venta_total']}", f"${datos['ganancia_total']}"])

    # Crear y estilizar tabla
    table = Table(data, colWidths=[200, 100, 100])
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(table_style)
    story.append(table)

    # Agregar ganancia total al final del reporte
    total_ganancia_parrafo = Paragraph(f"Total de Ganancia de Todos los Productos: ${total_ganancia}", styles['Heading2'])
    story.append(Spacer(1, 12))
    story.append(total_ganancia_parrafo)

    # Construir el PDF
    doc.build(story)
    return response

def reportes_ventas(request):
    try:
        # Obtener las fechas de los parámetros GET
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Si no se proporcionan fechas, usar la última semana como rango por defecto
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            today = datetime.now().date()
            start_date = today - timedelta(days=7)
            end_date = today

        # Obtener las ventas en el rango de fechas y ordenarlas por fecha descendente
        ventas_ultima_semana = Venta.objects.filter(fecha__date__gte=start_date, fecha__date__lte=end_date).order_by('-fecha')

        # Preparar datos para el reporte
        ventas = []
        for detalle in DetalleVenta.objects.filter(venta__in=ventas_ultima_semana):
            ventas.append({
                "fecha": detalle.fecha.strftime('%Y-%m-%d'),
                "tipo": detalle.tipo,
                "nombre_producto": detalle.nombre_producto,
                "cantidad": detalle.cantidad,
                "costo": detalle.costo,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": detalle.cantidad * detalle.precio_unitario,
                "ganancia": (detalle.cantidad * detalle.precio_unitario) - detalle.costo
            })

        # Contar los productos vendidos
        product_counter = Counter()
        for venta in ventas:
            product_counter[venta["nombre_producto"]] += venta["cantidad"]

        # Obtener el producto más vendido
        most_sold_product = product_counter.most_common(1)[0] if product_counter else ("N/A", 0)
        most_sold_product_data = {
            "nombre": most_sold_product[0],
            "cantidad": most_sold_product[1]
        }

        return JsonResponse({
            "ventas_semana": ventas,
            "most_sold_product": most_sold_product_data
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def actualizar_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        try:
            producto = Producto.objects.get(id=product_id)
            producto.cantidad += quantity

            if (producto.cantidad < 0):
                producto.cantidad -= quantity  # Revertir el cambio
                return JsonResponse({'success': False, 'message': 'No hay suficiente stock disponible.'})

            producto.save()
            return JsonResponse({'success': True})
        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

@csrf_exempt
def registrar_venta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        total = data.get('total', 0)
        service_id = data.get('id', None)  # Obtener el ID del servicio
        
        venta = Venta(total=total)
        venta.save()

        for item in items:
            tipo = item['type']
            cantidad = item['quantity']
            precio_unitario = item['unit_price']
            subtotal = cantidad * precio_unitario

            if tipo == 'Producto':
                producto = Producto.objects.get(id=item['id'])
                costof = producto.costo * cantidad
                producto.save()
                DetalleVenta.objects.create(
                    venta=venta,
                    tipo=tipo,
                    nombre_producto=producto.nombre,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal,
                    fecha=timezone.now(),
                    costo = costof
                )
            elif tipo == 'Reparación':
                if service_id:
                    try:
                        servicio = Servicio.objects.get(id=service_id)
                        AccionesServicio.objects.create(
                            servicio=servicio,
                            empleado=None,
                            descripcion="Se pago y entrego el equipo",
                            estado="Entregado",
                            costo=0,
                            foto_antes=None,
                            foto_despues=None
                        )
                    except Servicio.DoesNotExist:
                        logger.error(f'Service with id {service_id} not found')
                DetalleVenta.objects.create(
                    venta=venta,
                    tipo=tipo,
                    nombre_producto=servicio.descripcion,
                    cantidad=1,
                    precio_unitario=subtotal,
                    subtotal=subtotal,
                    fecha=timezone.now()
                )

        # Actualizar el servicio si existe
        if service_id:
            try:
                servicio = Servicio.objects.get(id=service_id)
                servicio.anticipo = servicio.total  
                servicio.pagado = True 
                servicio.estado = 'entregado'
                servicio.save()
                
            except Servicio.DoesNotExist:
                logger.error(f'Service with id {service_id} not found')
                return JsonResponse({'success': False, 'message': 'Servicio no encontrado.'})

        return JsonResponse({'success': True, 'venta_id': venta.id})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def cobros(request):
    return render(request, 'cobros_menu.html', {})

def cobros_pago(request):
    return render(request, 'cobros.html', {})

def cobros_gestion(request):
    return render(request, 'cobros_gestion.html', {})

def buscar_servicio_por_id(request, service_id):
    try:
        #servicio = Servicio.objects.get(id=service_id, pagado=False, estado='finalizado') or Servicio.objects.get(id=service_id, pagado=False, estado='Finalizado')
        servicio = Servicio.objects.get(id=service_id)
        if(servicio):
            if(servicio.pagado==False):
                if servicio.estado == 'finalizado' or servicio.estado =='Finalizado':
                    data = {
                        'success': True,
                        'service': {
                            'cliente': f'{servicio.cliente.nombre} {servicio.cliente.apellidos}',
                            'id': servicio.id,
                            'telefono': servicio.cliente.num_telefono,
                            'descripcion': f'Marca: {servicio.celular.marca}, Modelo: {servicio.celular.modelo}',
                            'reparacion': servicio.descripcion,
                            'cotizacion': str(servicio.cotizacion),
                            'costofinal': str(servicio.total),
                            'anticipo': str(servicio.anticipo) if servicio.anticipo else None,
                            'estado': str('Finalizado'),
                            'pagado': str('Pagado') if servicio.pagado else str('Pendiente de pago'),
                            'total': str(servicio.total - servicio.anticipo) if servicio.anticipo else str(servicio.total),
                        },
                        'error': str('Ok'),
                    }
                else:
                    if servicio.estado == 'en_proceso' or servicio.estado == 'ingresado':
                        data = {
                            'success': False,
                            'error': str('Noterminado'),
                        }
                    else:
                        data = {
                            'success': False,
                            'error': str('Estado'),
                        }
            else:
                data = {
                    'success': False,
                    'error': str('Pago'),
                }
    except Servicio.DoesNotExist:
        data = {'success': False,
                'error': str('ID')}

    return JsonResponse(data)

def buscar_servicio_por_nombre(request):
    client_name = request.GET.get('name', '')
    try:
        cliente = Cliente.objects.filter(nombre__icontains=client_name).first()
        if cliente:
            #servicio = Servicio.objects.filter(cliente=cliente, pagado=False, estado='finalizado').first() or Servicio.objects.filter(cliente=cliente, pagado=False, estado='Finalizado').first()
            servicio = Servicio.objects.filter(cliente=cliente, pagado=False).first()
            if(servicio):
                data = {
                    'success': True,
                    'service': {
                        'cliente': f'{servicio.cliente.nombre} {servicio.cliente.apellidos}',
                        'id': servicio.id,
                        'telefono': servicio.cliente.num_telefono,
                        'descripcion': f'Marca: {servicio.celular.marca}, Modelo: {servicio.celular.modelo}',
                        'reparacion': servicio.descripcion,
                        'cotizacion': str(servicio.cotizacion),
                        'anticipo': str(servicio.anticipo) if servicio.anticipo else None,
                        'estado': str('Finalizado'),
                        'pagado': str('Pagado') if servicio.pagado else str('Pendiente de pago'),
                        'total': str(servicio.cotizacion - servicio.anticipo) if servicio.anticipo else str(servicio.cotizacion),
                    },
                        'error': str('Ok'),
                }
            else:
                data = {
                    'success': False,
                    'error': str('Pago'),
                }
        else:
            data = {
                    'success': False,
                    'error': str('Cliente'),
                }
    except Cliente.DoesNotExist:
        data = {'success': False,
                'error': str('ID')}

    return JsonResponse(data)

def buscar_producto(request):
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query, activo=True)
    else:
        productos = Producto.objects.all().filter(activo=True)  # Devolver todos los productos si la consulta está vacía
    data = list(productos.values('id', 'nombre', 'precio'))
    return JsonResponse(data, safe=False)
    