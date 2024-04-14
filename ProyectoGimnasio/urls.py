"""
URL configuration for ProyectoGimnasio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from OxigenoGYMAPP import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_gym'),
    path('salir/', views.logout_view, name='salir_gym'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('historial/<int:id_cliente>/', views.ver_historial, name='ver_historial'),  # Cambiado 'dni' a 'id_cliente'
    path('clientes/editar/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),  # Cambiado 'dni' a 'id_cliente'
    path('clientes/eliminar/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),  # Cambiado 'dni' a 'id_cliente'
    path('live_search/', views.live_search, name='live_search'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('clientes/renovar/<int:id_cliente>/', views.renovar_cuota, name='renovar_couta'),

    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)