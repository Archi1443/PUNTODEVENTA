from django.urls import path
from . import views
from .views import inventario


urlpatterns = [
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/registro', views.inventario_registro, name='inventario_registro'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),
    path('actualizar_cantidad_producto/', views.actualizar_cantidad_producto, name='actualizar_cantidad_producto'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
    path('inventario/', inventario, name='inventario'),
    path('inventario/modificar/<int:id>/', views.inventario_editar, name='inventario_editar'),
]
