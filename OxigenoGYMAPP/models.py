from django.db import models
from datetime import datetime, timedelta

# Funciones para los valores por defecto
def default_fecha_inicio():
    return datetime.now()

def default_fecha_fin():
    return datetime.now() + timedelta(days=30)

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=100)
    dni = models.CharField(primary_key=True,max_length=20, unique=True)
    apodo = models.CharField(max_length=50, blank=True)
    fecha_inicio_cuota = models.DateField(default=default_fecha_inicio, blank=True, null=True)
    fecha_fin_cuota = models.DateField(default=default_fecha_fin, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

    def save(self, *args, **kwargs):
        # Convertir las fechas de string a date si es necesario
        if isinstance(self.fecha_inicio_cuota, str) and '/' in self.fecha_inicio_cuota:
            day, month, year = self.fecha_inicio_cuota.split('/')
            self.fecha_inicio_cuota = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
        
        if isinstance(self.fecha_fin_cuota, str) and '/' in self.fecha_fin_cuota:
            day, month, year = self.fecha_fin_cuota.split('/')
            self.fecha_fin_cuota = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()

        super(Cliente, self).save(*args, **kwargs)
