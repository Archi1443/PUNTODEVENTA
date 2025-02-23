from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_gestion, name='clientes'),
    path('clientes/registro/', views.clientes_registro, name='clientes_registro'),
    path('clientes/modificar/<int:cliente_id>/', views.clientes_modificar, name='clientes_modificar'),
    path('clientes/borrar/<int:cliente_id>/', views.clientes_borrar, name='clientes_borrar'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
]
