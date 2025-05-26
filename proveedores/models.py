from django.db import models

class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15,blank=True,null=True)
    correo = models.EmailField(max_length=50,blank=True,null=True)
    direccion = models.CharField(max_length=150,blank=True,null=True)
    calificacion = models.IntegerField(max_length=2,blank=True,null=True)
    

    def __str__(self):
        return f"{self.nombre}"