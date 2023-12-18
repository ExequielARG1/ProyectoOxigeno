from django.db import models
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

def default_fecha_inicio():
    return datetime.now().date()

def default_fecha_fin():
    return (datetime.now() + timedelta(days=30)).date()

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    apodo = models.CharField(max_length=50, blank=True)
    fecha_inicio_cuota = models.DateField(default=default_fecha_inicio, blank=True, null=True)
    fecha_fin_cuota = models.DateField(default=default_fecha_fin, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

class CuotaHistorial(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_inicio_cuota = models.DateField()
    fecha_fin_cuota = models.DateField()

    class Meta:
        unique_together = ['cliente', 'fecha_inicio_cuota', 'fecha_fin_cuota']

    def __str__(self):
        return f"{self.cliente.nombre_completo} - {self.fecha_inicio_cuota} a {self.fecha_fin_cuota}"

@receiver(post_save, sender=Cliente)
def crear_historial_cuotas(sender, instance, created, **kwargs):
    # Verificar si es un nuevo cliente
    if created:
        CuotaHistorial.objects.create(
            cliente=instance,
            fecha_inicio_cuota=instance.fecha_inicio_cuota,
            fecha_fin_cuota=instance.fecha_fin_cuota
        )
    else:
        # Si el cliente ya existe, verificar si las fechas de cuota han cambiado
        if not CuotaHistorial.objects.filter(cliente=instance, fecha_inicio_cuota=instance.fecha_inicio_cuota, fecha_fin_cuota=instance.fecha_fin_cuota).exists():
            CuotaHistorial.objects.create(
                cliente=instance,
                fecha_inicio_cuota=instance.fecha_inicio_cuota,
                fecha_fin_cuota=instance.fecha_fin_cuota
            )