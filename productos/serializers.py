from rest_framework import serializers

from almacenes.models import Almacen
from almacenes.serializers import AlmacenSerializer
from categorias.models import Categoria
from categorias.serializers import CategoriaSerializer
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    almacen_nombre = serializers.CharField(source='almacen.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria','categoria_nombre','almacen' ,'almacen_nombre', ]
