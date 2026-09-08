from django import forms
from .models import NodoServidor, IncidenciaServidor


class NodoServidorForm(forms.ModelForm):
    class Meta:
        model = NodoServidor
        fields = ['nombre_host', 'direccion_ip', 'motor_contenedores', 'proxy_inverso', 'en_produccion']


class IncidenciaServidorForm(forms.ModelForm):
    class Meta:
        model = IncidenciaServidor
        fields = ['titulo', 'descripcion', 'severidad', 'resuelto']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Fallo en el contenedor de la API',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el fallo operativo detectado...',
            }),
            'severidad': forms.Select(attrs={'class': 'form-select'}),
            'resuelto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }