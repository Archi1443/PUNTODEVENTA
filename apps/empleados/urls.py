from django.urls import path
from . import views

urlpatterns = [
    path('empleados/', views.empleados_gestion, name='empleados_gestion'),
    path('empleados/registro/', views.empleados_registro, name='empleados_registro'),
    path('empleados/modificar_usuario_empleado/<int:id>/', views.modificar_usuario_empleado, name='modificar_usuario_empleado'),
    path('empleados/modificar_datos_empleado/<int:id>/', views.modificar_datos_empleado, name='modificar_datos_empleado'),
    path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='empleados_eliminar'),
    path('buscar_empleado/', views.buscar_empleado, name='buscar_empleado'),
]
