from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NodoServidorForm, IncidenciaServidorForm, MantenimientoForm
from .models import NodoServidor, IncidenciaServidor, MantenimientoNodo


class MantenimientoListView(ListView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_list.html'
    context_object_name = 'mantenimientos'


class MantenimientoDetailView(DetailView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_detail.html'
    context_object_name = 'mantenimiento'


class MantenimientoCreateView(CreateView):
    model = MantenimientoNodo
    form_class = MantenimientoForm
    template_name = 'infraestructura/mantenimiento_form.html'
    success_url = reverse_lazy('lista_mantenimientos')


class MantenimientoUpdateView(UpdateView):
    model = MantenimientoNodo
    form_class = MantenimientoForm
    template_name = 'infraestructura/mantenimiento_form.html'
    success_url = reverse_lazy('lista_mantenimientos')


class MantenimientoDeleteView(DeleteView):
    model = MantenimientoNodo
    template_name = 'infraestructura/mantenimiento_confirm_delete.html'
    success_url = reverse_lazy('lista_mantenimientos')


def crear_incidencia(request, pk):
    servidor = get_object_or_404(NodoServidor, pk=pk)
    if request.method == 'POST':
        form = IncidenciaServidorForm(request.POST)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.servidor = servidor
            incidencia.save()
            messages.success(request, 'Incidencia registrada correctamente.')
            return redirect('detalle_servidor', pk=servidor.pk)
    else:
        form = IncidenciaServidorForm()
    return render(request, 'infraestructura/crear_incidencia.html', {'form': form, 'servidor': servidor})


def detalle_incidencia(request, pk):
    incidencia = get_object_or_404(IncidenciaServidor, pk=pk)
    return render(request, 'infraestructura/detalle_incidencia.html', {'incidencia': incidencia})


def resolver_incidencia(request, pk):
    incidencia = get_object_or_404(IncidenciaServidor, pk=pk)
    if request.method == 'POST':
        incidencia.resuelto = True
        incidencia.save()
        messages.success(request, f'La incidencia "{incidencia.titulo}" fue marcada como resuelta.')
        return redirect('detalle_servidor', pk=incidencia.servidor.pk)
    return render(request, 'infraestructura/resolver_incidencia.html', {'incidencia': incidencia})


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