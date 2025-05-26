from rest_framework import serializers

from sucursales.models import Sucursal
from .models import Almacen
from sucursales.serializers import SucursalSerializer

class AlmacenSerializer(serializers.ModelSerializer):
    sucursal = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all())
    sucursal_info = SucursalSerializer(source='sucursal', read_only=True)

    class Meta:
        model = Almacen
        fields = ['id', 'nombre', 'sucursal', 'sucursal_info']