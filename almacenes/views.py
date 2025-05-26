from rest_framework.viewsets import ModelViewSet
from .models import Almacen
from .serializers import AlmacenSerializer

class AlmacenViewSet(ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
