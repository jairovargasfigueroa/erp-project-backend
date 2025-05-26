from django.db import models

class Cliente(models.Model):
    ci = models.CharField(max_length=20, unique=True)  # Puede ser NIT también
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} , {self.ci}"
