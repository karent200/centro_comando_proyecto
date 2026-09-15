from django.urls import path, include
from rest_framework.routers import DefaultRouter
from infraestructura.views import (
    lista_servidores,
    detalle_servidor,
    crear_servidor,
    editar_servidor,
    eliminar_servidor,
    crear_incidencia,
    detalle_incidencia,
    resolver_incidencia,
    MantenimientoListView,
    MantenimientoDetailView,
    MantenimientoCreateView,
    MantenimientoUpdateView,
    MantenimientoDeleteView,
)
from infraestructura.api import (
    NodoServidorViewSet,
    IncidenciaServidorViewSet,
    RegistroAuditoriaViewSet,
    MantenimientoNodoViewSet,
)

router = DefaultRouter()
router.register(r'servidores', NodoServidorViewSet, basename='servidor')
router.register(r'incidencias', IncidenciaServidorViewSet, basename='incidencia')
router.register(r'auditorias', RegistroAuditoriaViewSet, basename='auditoria')
router.register(r'mantenimientos', MantenimientoNodoViewSet, basename='mantenimiento')

urlpatterns = [
    path('', lista_servidores, name='home_servidores'),
    path('servidor/<int:pk>/', detalle_servidor, name='detalle_servidor'),
    path('servidor/nuevo/', crear_servidor, name='crear_servidor'),
    path('servidor/<int:pk>/editar/', editar_servidor, name='editar_servidor'),
    path('servidor/<int:pk>/eliminar/', eliminar_servidor, name='eliminar_servidor'),
    path('servidor/<int:pk>/incidencias/nueva/', crear_incidencia, name='crear_incidencia'),
    path('incidencia/<int:pk>/', detalle_incidencia, name='detalle_incidencia'),
    path('incidencia/<int:pk>/resolver/', resolver_incidencia, name='resolver_incidencia'),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]

urlpatterns += [
    path('mantenimientos/', MantenimientoListView.as_view(), name='lista_mantenimientos'),
    path('mantenimientos/<int:pk>/', MantenimientoDetailView.as_view(), name='detalle_mantenimiento'),
    path('mantenimientos/nuevo/', MantenimientoCreateView.as_view(), name='crear_mantenimiento'),
    path('mantenimientos/<int:pk>/editar/', MantenimientoUpdateView.as_view(), name='editar_mantenimiento'),
    path('mantenimientos/<int:pk>/eliminar/', MantenimientoDeleteView.as_view(), name='eliminar_mantenimiento'),
]