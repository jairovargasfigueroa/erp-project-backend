from django.db import models

from sucursales.models import Sucursal

class Almacen(models.Model):
    nombre = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL,null=True,blank=True, related_name='almacenes')

    def __str__(self):
        return f"{self.nombre} ({self.sucursal.nombre})"