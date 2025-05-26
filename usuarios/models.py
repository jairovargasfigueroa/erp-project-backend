from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    # Campos adicionales para el modelo de usuario
    direccion = models.CharField(max_length=255,blank=True, null=True)
    telefono = models.CharField(max_length=15,blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
