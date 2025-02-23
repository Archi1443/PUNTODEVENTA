from django.urls import path
from . import views
#from .views import enviar_mensaje_whatsapp


urlpatterns = [
    path('servicios/', views.servicios_gestion, name='servicios_gestion'),
    path('servicios/registro/', views.servicios_registro, name='servicios_registro'),
    path('servicios/clientes/registro/', views.servicios_clientes_registro, name='servicios_clientes_registro'),
    path('servicios/consulta/<int:id>/', views.servicios_consulta, name='servicios_consulta'),
    path('servicios/filtrar_servicios/', views.filtrar_servicios, name='filtrar_servicios'), 
    path('servicios/modificar/<int:id>/', views.servicios_editar, name='servicios_editar'),
    path('servicios/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
    path('servicios/acciones/<int:id>/', views.servicios_acciones, name='servicios_acciones'),
    path('servicios/acciones/registro/<int:id>/', views.acciones_registro, name='acciones_registro'),
    path('eliminar_accion/', views.eliminar_accion, name='eliminar_accion'),
    path('servicios/acciones/modificar/<int:id>/', views.acciones_editar, name='acciones_editar'),
    path('verificar_cliente/', views.verificar_cliente, name='verificar_cliente'),
]
