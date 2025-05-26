from django.db import models
from almacenes.models import Almacen
from categorias.models import Categoria

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL,null=True,blank=True, related_name='productos')
    almacen = models.ForeignKey(Almacen, on_delete=models.SET_NULL,null=True,blank=True, related_name='productos')
    
    def __str__(self):
        return self.nombre
