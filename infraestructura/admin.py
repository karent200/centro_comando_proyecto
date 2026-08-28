from django.contrib import admin
from django.contrib import messages
from .models import NodoServidor, RegistroAuditoria


class RegistroAuditoriaInline(admin.TabularInline):
    model = RegistroAuditoria
    extra = 0
    readonly_fields = ('fecha_evento',)


@admin.register(NodoServidor)
class NodoServidorAdmin(admin.ModelAdmin):
    inlines = [RegistroAuditoriaInline]
    # Columnas que se mostrarán en la tabla principal
    list_display = ('nombre_host', 'direccion_ip', 'motor_contenedores', 'proxy_inverso', 'en_produccion')
    # Filtros laterales para hacer búsquedas rápidas
    list_filter = ('motor_contenedores', 'proxy_inverso', 'en_produccion')
    # Barra de búsqueda superior
    search_fields = ('nombre_host', 'direccion_ip')
    # Orden por defecto
    ordering = ('-fecha_despliegue',)
    # Acciones masivas personalizadas
    actions = ['marcar_como_produccion', 'marcar_como_mantenimiento']

    @admin.action(description="Activar Producción Masiva")
    def marcar_como_produccion(self, request, queryset):
        """Cambia el estado de producción a True para los nodos seleccionados."""
        actualizados = queryset.update(en_produccion=True)
        self.message_user(
            request,
            f"{actualizados} nodo(s) marcado(s) como en PRODUCCIÓN.",
            messages.SUCCESS,
        )

    @admin.action(description="Poner en Mantenimiento")
    def marcar_como_mantenimiento(self, request, queryset):
        """Cambia el estado de producción a False para aislar nodos."""
        actualizados = queryset.update(en_produccion=False)
        self.message_user(
            request,
            f"{actualizados} nodo(s) puesto(s) en MANTENIMIENTO.",
            messages.WARNING,
        )


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('servidor', 'detalles', 'fecha_evento')
    list_filter = ('fecha_evento', 'servidor')
    search_fields = ('servidor__nombre_host', 'detalles')
    ordering = ('-fecha_evento',)
    readonly_fields = ('fecha_evento',)
