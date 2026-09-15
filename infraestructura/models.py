import ipaddress
from django.db import models
from django.core.exceptions import ValidationError


def validar_ip_corporativa(value):
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError("Formato de dirección IP no válido.")

    # Redes privadas no autorizadas
    rango_pruebas = ipaddress.ip_network("192.168.100.0/24")
    rango_no_autorizado = ipaddress.ip_network("10.0.1.0/24")

    if ip in rango_pruebas:
        raise ValidationError(
            "Las direcciones IP en el segmento 192.168.100.x están "
            "reservadas para pruebas internas de aislamiento."
        )

    if ip in rango_no_autorizado:
        raise ValidationError(
            "Las direcciones IP en el segmento 10.0.1.x no están "
            "autorizadas para nodos de producción."
        )

    # Reservadas por RFC 6890 / IANA (no usable como host)
    if ip.is_reserved:
        raise ValidationError("La dirección IP pertenece a un rango reservado por IANA.")

    if ip.is_link_local:
        raise ValidationError("Las direcciones link-local (169.254.x.x) no son válidas.")


class NodoServidor(models.Model):
    # Opciones predefinidas para el panel
    MOTORES_CONTENEDOR = [
        ('docker', 'Docker'),
        ('podman', 'Podman'),
        ('lxc', 'LXC Linux Containers'),
        ('ninguno', 'Sin contenedores'),
    ]

    nombre_host = models.CharField(max_length=100, unique=True, verbose_name="Hostname")
    direccion_ip = models.GenericIPAddressField(
        verbose_name="Dirección IP",
        validators=[validar_ip_corporativa]
    )
    motor_contenedores = models.CharField(
        max_length=20,
        choices=MOTORES_CONTENEDOR,
        default='podman',
        verbose_name="Motor de Contenedores"
    )
    proxy_inverso = models.BooleanField(default=True, verbose_name="¿Enrutado por Nginx?")
    en_produccion = models.BooleanField(default=True, verbose_name="Estado Producción")
    fecha_despliegue = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_host} [{self.direccion_ip}]"

    class Meta:
        verbose_name = "Nodo de Servidor"
        verbose_name_plural = "Flota de Servidores"


class IncidenciaServidor(models.Model):
    SEVERIDAD_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='incidencias',
    )
    titulo = models.CharField(max_length=150, verbose_name="Título del Fallo")
    descripcion = models.TextField(verbose_name="Descripción")
    severidad = models.CharField(
        max_length=10,
        choices=SEVERIDAD_CHOICES,
        default='media',
        verbose_name="Severidad"
    )
    resuelto = models.BooleanField(default=False, verbose_name="¿Resuelto?")
    fecha_evento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "resuelta" if self.resuelto else "activa"
        return f"Incidencia {self.titulo} ({self.get_severidad_display()}) - {estado}"

    class Meta:
        verbose_name = "Incidencia de Servidor"
        verbose_name_plural = "Alertas e Incidencias"
        ordering = ('-fecha_evento',)


class RegistroAuditoria(models.Model):
    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='auditorias'
    )
    detalles = models.TextField(verbose_name="Detalle del Evento")
    fecha_evento = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Auditoría de {self.servidor.nombre_host} - {self.fecha_evento:%Y-%m-%d %H:%M}"


    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ('-fecha_evento',)


class MantenimientoNodo(models.Model):
    TIPO_TAREA = [
        ('actualizacion', 'Actualización de Sistema'),
        ('backup', 'Respaldo de Base de Datos'),
        ('seguridad', 'Parche de Seguridad'),
        ('hardware', 'Revisión de Hardware'),
    ]

    servidor = models.ForeignKey(
        NodoServidor,
        on_delete=models.CASCADE,
        related_name='mantenimientos',
        verbose_name="Servidor Asignado"
    )
    titulo_tarea = models.CharField(max_length=150, verbose_name="Título del Mantenimiento")
    descripcion_tecnica = models.TextField(verbose_name="Descripción de la Tarea")
    tipo = models.CharField(max_length=30, choices=TIPO_TAREA, default='actualizacion', verbose_name="Tipo de Tarea")
    completado = models.BooleanField(default=False, verbose_name="¿Tarea Ejecutada?")
    fecha_programada = models.DateTimeField(verbose_name="Fecha y Hora Programada")

    def __str__(self):
        return f"{self.titulo_tarea} - {self.servidor.nombre_host}"

    class Meta:
        verbose_name = "Mantenimiento de Servidor"
        verbose_name_plural = "Programación de Mantenimientos"
