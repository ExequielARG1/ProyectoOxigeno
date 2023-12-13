from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
# Create your views here.
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
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes, 'form': ClienteForm()})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes, 'form': form})

def editar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'nombre_completo': cliente.nombre_completo,
            'apodo': cliente.apodo,
            'dni': cliente.dni,
        }
        return JsonResponse(data)

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form': form, 'clientes': clientes})

def eliminar_cliente(request, dni):
    cliente = get_object_or_404(Cliente, dni=dni)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return redirect('listar_clientes')