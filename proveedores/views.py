from rest_framework.viewsets import ModelViewSet

from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializers

class ProveedorViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializers
    
