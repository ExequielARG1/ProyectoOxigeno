from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    apodo = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre_completo