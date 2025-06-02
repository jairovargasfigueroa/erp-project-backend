from rest_framework.viewsets import ModelViewSet
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer

