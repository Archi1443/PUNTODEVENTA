from django.urls import path
from . import views

urlpatterns = [
    path('cobros/', views.cobros, name='cobros'),
    path('cobros/pago', views.cobros_pago, name='cobros_pago'),
    path('cobros/reportes/', views.reportes_ventas, name='reportes_ventas'),
    path('cobros/gestion', views.cobros_gestion, name='cobros_gestion'),
    path('buscar_servicio_por_id/<int:service_id>/', views.buscar_servicio_por_id, name='buscar_servicio_por_id'),
    path('buscar_servicio_por_nombre/', views.buscar_servicio_por_nombre, name='buscar_servicio_por_nombre'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),
    path('actualizar_stock/', views.actualizar_stock, name='actualizar_stock'),
    path('registrar_venta/', views.registrar_venta, name='registrar_venta'),
    path('cobros/reportes/pdf/', views.generar_reporte_ventas, name='generar_reporte_ventas'),
    ]

