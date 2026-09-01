from django.shortcuts import render
from .models import NodoServidor

def lista_servidores(request):
	servidores = NodoServidor.objects.all()
	contexto = {'servidores': servidores}
	return render(request, 'infraestructura/index.html', contexto)