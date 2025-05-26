from rest_framework import serializers

from almacenes.models import Almacen
from almacenes.serializers import AlmacenSerializer
from categorias.models import Categoria
from categorias.serializers import CategoriaSerializer
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    # categoria_info = CategoriaSerializer(source='categoria', read_only=True)
    almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    # almacen_info = AlmacenSerializer(source='almacen', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria',  'almacen', ]
