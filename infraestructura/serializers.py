from rest_framework import serializers
from .models import NodoServidor, IncidenciaServidor, RegistroAuditoria, MantenimientoNodo


class NodoServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodoServidor
        fields = '__all__'


class IncidenciaServidorSerializer(serializers.ModelSerializer):
    servidor_hostname = serializers.CharField(source='servidor.nombre_host', read_only=True)

    class Meta:
        model = IncidenciaServidor
        fields = '__all__'
        extra_kwargs = {
            'servidor': {'queryset': NodoServidor.objects.all()},
        }


class RegistroAuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAuditoria
        fields = '__all__'


class MantenimientoNodoSerializer(serializers.ModelSerializer):
    servidor_hostname = serializers.CharField(source='servidor.nombre_host', read_only=True)

    class Meta:
        model = MantenimientoNodo
        fields = '__all__'
        extra_kwargs = {
            'servidor': {'queryset': NodoServidor.objects.all()},
        }