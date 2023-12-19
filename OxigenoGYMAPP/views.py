from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Cliente, CuotaHistorial
from .forms import ClienteForm, CuotaHistorialForm
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.db.models import Q
from django.template.loader import render_to_string


def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Nombre de usuario o contraseña no válidos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña no válidos.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login_gym')
def listar_clientes(request):
    # Obtener todos los clientes
    clientes = Cliente.objects.all()

    # Aplicar búsqueda en tiempo real
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(
            Q(nombre_completo__icontains=query) |
            Q(apodo__icontains=query) |
            Q(dni__icontains=query)
        )

    # Aplicar paginación (mostrar 5 clientes por página)
    paginator = Paginator(clientes, 2)
    page = request.GET.get('page')

    try:
        clientes_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        clientes_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por ejemplo, 9999), mostrar la última página
        clientes_pagina = paginator.page(paginator.num_pages)

    historiales_cuotas = CuotaHistorial.objects.all()
    form_cliente = ClienteForm()  # Utiliza el formulario de Django
    return render(request, 'clientes.html', {'clientes': clientes_pagina, 'historiales_cuotas': historiales_cuotas, 'form_cliente': form_cliente, 'historial_form': CuotaHistorialForm()})


def ver_historial(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        historial_cuotas = CuotaHistorial.objects.filter(cliente=cliente)

        cliente_nombre = cliente.nombre_completo if cliente else "Cliente Desconocido"

        data = [
            {'fecha_inicio_cuota': str(historial.fecha_inicio_cuota), 'fecha_fin_cuota': str(historial.fecha_fin_cuota)}
            for historial in historial_cuotas
        ]

        response_data = {'cliente_nombre': cliente_nombre, 'historial': data}
        return JsonResponse(response_data, safe=False)
    except Cliente.DoesNotExist:
        return JsonResponse({'cliente_nombre': 'Cliente no encontrado', 'historial': []}, safe=False)
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('listar_clientes')
            except IntegrityError:
                existing_client = Cliente.objects.get(dni=form.cleaned_data['dni'])
                messages.error(request, f'El cliente con DNI {existing_client.dni} ya existe.')
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ClienteForm()

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes, 'form': form})

@transaction.atomic
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    try:
        if request.method == 'POST':
            form_cliente = ClienteForm(request.POST, instance=cliente)
            form_cuota = CuotaHistorialForm(request.POST)

            if form_cliente.is_valid() and form_cuota.is_valid():
                form_cliente.save()

                # Intenta obtener un registro existente o crear uno nuevo
                cuota, created = CuotaHistorial.objects.get_or_create(
                    cliente=cliente,
                    fecha_inicio_cuota=form_cuota.cleaned_data['fecha_inicio_cuota'],
                    defaults={'fecha_fin_cuota': form_cuota.cleaned_data['fecha_fin_cuota']}
                )

                if not created:
                    # Si el registro ya existe, actualiza las fechas
                    cuota.fecha_fin_cuota = form_cuota.cleaned_data['fecha_fin_cuota']
                    cuota.save()

                return redirect('listar_clientes')
        else:
            form_cliente = ClienteForm(instance=cliente)
            form_cuota = CuotaHistorialForm()

        # Manejar la petición GET y AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
                'id_cliente': cliente.id_cliente,
                'dni': cliente.dni,
                'nombre_completo': cliente.nombre_completo,
                'apodo': cliente.apodo,
                'fecha_inicio_cuota': cliente.fecha_inicio_cuota.strftime('%Y-%m-%d') if cliente.fecha_inicio_cuota else '',
                'fecha_fin_cuota': cliente.fecha_fin_cuota.strftime('%Y-%m-%d') if cliente.fecha_fin_cuota else '',
            }
            return JsonResponse(data)

    except Exception as e:
        # Manejar la excepción
        return JsonResponse({'error': str(e)})

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form_cliente': form_cliente, 'form_cuota': form_cuota, 'clientes': clientes})

@transaction.atomic
def eliminar_cliente(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        if request.method == 'POST':
            # Eliminar manualmente las entradas en CuotaHistorial
            CuotaHistorial.objects.filter(cliente=cliente).delete()
            cliente.delete()
            return redirect('listar_clientes')
    except Cliente.DoesNotExist:
        pass
    return HttpResponseServerError("Error interno al eliminar el cliente.")




from django.http import JsonResponse

def live_search(request):
    try:
        query = request.GET.get('q', '')
        results = Cliente.objects.filter(
            nombre_completo__icontains=query) | Cliente.objects.filter(
            apodo__icontains=query) | Cliente.objects.filter(
            dni__icontains=query)

        data = [{'id_cliente': cliente.id_cliente, 'nombre_completo': cliente.nombre_completo, 'apodo': cliente.apodo, 'dni': cliente.dni} for cliente in results]

        return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error en live_search: {str(e)}")
        return JsonResponse({'error': 'Error en el servidor'}, status=500)
