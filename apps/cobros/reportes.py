from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from collections import defaultdict

# Datos de ejemplo
ventas = [
    {"fecha": "2023-06-24", "nombre_producto": "Funda iPhone 13", "cantidad": 2, "costo": 2500},
    {"fecha": "2023-06-25", "nombre_producto": "Funda Samsung Galaxy S6", "cantidad": 1, "costo": 3000},
    {"fecha": "2023-06-25", "nombre_producto": "Funda Huawei K9s", "cantidad": 3, "costo": 2500},
    {"fecha": "2023-06-26", "nombre_producto": "Cargador iPhone 7", "cantidad": 1, "costo": 8000},
    {"fecha": "2023-06-26", "nombre_producto": "Cargador iPhone 8", "cantidad": 1, "costo": 9000},
    {"fecha": "2023-06-25", "nombre_producto": "Cargador Samsung Galaxy S7", "cantidad": 1, "costo": 7000},
]

def generar_reporte(fecha_inicio, fecha_fin):
    doc = SimpleDocTemplate("reporte_productos_vendidos_bonito.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Título del reporte
    titulo = Paragraph("Reporte de Productos Vendidos - Tech Solutions", styles['Title'])
    story.append(titulo)
    story.append(Spacer(1, 12))

    # Fechas del reporte
    subtitulo = Paragraph(f"Desde: {fecha_inicio} Hasta: {fecha_fin}", styles['Heading2'])
    story.append(subtitulo)
    story.append(Spacer(1, 12))

    # Filtrar y resumir ventas
    ventas_filtradas = [
        venta for venta in ventas
        if datetime.strptime(venta['fecha'], '%Y-%m-%d').date() >= datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        and datetime.strptime(venta['fecha'], '%Y-%m-%d').date() <= datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    ]
    resumen_ventas = defaultdict(lambda: {'cantidad_total': 0, 'ganancia_total': 0})
    total_ganancia = 0  # Inicializar total de ganancia
    for venta in ventas_filtradas:
        producto = venta['nombre_producto']
        resumen_ventas[producto]['cantidad_total'] += venta['cantidad']
        ganancia_producto = venta['cantidad'] * venta['costo']
        resumen_ventas[producto]['ganancia_total'] += ganancia_producto
        total_ganancia += ganancia_producto  # Sumar a total de ganancia

    # Datos para la tabla
    data = [["Producto", "Cantidad Total", "Ganancia Total"]]
    for producto, datos in resumen_ventas.items():
        data.append([producto, datos['cantidad_total'], f"${datos['ganancia_total']}"])

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

# Configuración de fechas para el reporte
fecha_inicio = '2023-06-24'
fecha_fin = '2023-06-26'
generar_reporte(fecha_inicio, fecha_fin)
