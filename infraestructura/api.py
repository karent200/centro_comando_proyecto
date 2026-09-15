from rest_framework import viewsets
from .models import NodoServidor, IncidenciaServidor, RegistroAuditoria, MantenimientoNodo
from .serializers import (
    NodoServidorSerializer,
    IncidenciaServidorSerializer,
    RegistroAuditoriaSerializer,
    MantenimientoNodoSerializer,
)


class NodoServidorViewSet(viewsets.ModelViewSet):
    """
    API REST de la flota de servidores.
    GET → listar / recuperar, POST → crear, PUT → reemplazar, PATCH → actualizar parcialmente, DELETE → eliminar.
    """
    queryset = NodoServidor.objects.all()
    serializer_class = NodoServidorSerializer
    search_fields = ['nombre_host', 'direccion_ip']
    ordering_fields = ['nombre_host', 'fecha_despliegue']


class IncidenciaServidorViewSet(viewsets.ModelViewSet):
    """
    API REST de alertas e incidencias operativas.
    Soporta filtrar por servidor: /api/incidencias/?servidor=1
    """
    queryset = IncidenciaServidor.objects.select_related('servidor').all()
    serializer_class = IncidenciaServidorSerializer
    filterset_fields = ['severidad', 'resuelto', 'servidor']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['fecha_evento', 'severidad']


class RegistroAuditoriaViewSet(viewsets.ModelViewSet):
    """
    API REST de los registros de auditoría.
    """
    queryset = RegistroAuditoria.objects.select_related('servidor').all()
    serializer_class = RegistroAuditoriaSerializer
    filterset_fields = ['servidor']
    ordering_fields = ['fecha_evento']


class MantenimientoNodoViewSet(viewsets.ModelViewSet):
    """
    API REST de los mantenimientos técnicos programados.
    Soporta filtrar por servidor, tipo y estado: /api/mantenimientos/?servidor=1&tipo=backup&completado=false
    """
    queryset = MantenimientoNodo.objects.select_related('servidor').all()
    serializer_class = MantenimientoNodoSerializer
    filterset_fields = ['servidor', 'tipo', 'completado']
    search_fields = ['titulo_tarea', 'descripcion_tecnica']
    ordering_fields = ['fecha_programada']