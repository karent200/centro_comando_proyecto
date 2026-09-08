from django.urls import path
from infraestructura.views import (
    lista_servidores,
    detalle_servidor,
    crear_servidor,
    editar_servidor,
    eliminar_servidor,
    crear_incidencia,
    detalle_incidencia,
    resolver_incidencia,
)

urlpatterns = [
    path('', lista_servidores, name='home_servidores'),
    path('servidor/<int:pk>/', detalle_servidor, name='detalle_servidor'),
    path('servidor/nuevo/', crear_servidor, name='crear_servidor'),
    path('servidor/<int:pk>/editar/', editar_servidor, name='editar_servidor'),
    path('servidor/<int:pk>/eliminar/', eliminar_servidor, name='eliminar_servidor'),
    path('servidor/<int:pk>/incidencias/nueva/', crear_incidencia, name='crear_incidencia'),
    path('incidencia/<int:pk>/', detalle_incidencia, name='detalle_incidencia'),
    path('incidencia/<int:pk>/resolver/', resolver_incidencia, name='resolver_incidencia'),
]