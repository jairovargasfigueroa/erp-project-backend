from rest_framework.viewsets import ModelViewSet
from .models import Sucursal
from .serializers import SucursalSerializer

class SucursalViewSet(ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
