from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)

urlpatterns = router.urls