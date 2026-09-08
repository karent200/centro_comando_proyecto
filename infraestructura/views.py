from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import NodoServidorForm
from .models import NodoServidor


def eliminar_servidor(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        nodo.delete()
        messages.success(request, f'El servidor {nodo.nombre_host} fue eliminado.')
        return redirect('home_servidores')
    return render(request, 'infraestructura/eliminar_servidor.html', {'nodo': nodo})


def editar_servidor(request, pk):
    nodo = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        form = NodoServidorForm(request.POST, instance=nodo)
        if form.is_valid():
            form.save()
            messages.success(request, f'El servidor {nodo.nombre_host} fue actualizado.')
            return redirect('detalle_servidor', pk=nodo.pk)
    else:
        form = NodoServidorForm(instance=nodo)
    return render(request, 'infraestructura/editar_servidor.html', {'form': form, 'nodo': nodo})


def crear_servidor(request):
    if request.method == 'POST':
        form = NodoServidorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servidor creado correctamente.')
            return redirect('home_servidores')
    else:
        form = NodoServidorForm()
    return render(request, 'infraestructura/crear_servidor.html', {'form': form})


def detalle_servidor(request, pk):
    servidor = get_object_or_404(NodoServidor, pk=pk)
    contexto = {'nodo': servidor}
    return render(request, 'infraestructura/detalle.html', contexto)


def lista_servidores(request):
    servidores = NodoServidor.objects.all()
    contexto = {'servidores': servidores}
    return render(request, 'infraestructura/index.html', contexto)