from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet)

urlpatterns = router.urls