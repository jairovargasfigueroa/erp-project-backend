from rest_framework.routers import DefaultRouter
from .views import AlmacenViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenViewSet)

urlpatterns = router.urls