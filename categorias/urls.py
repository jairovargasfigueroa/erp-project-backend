from rest_framework.routers import DefaultRouter
from .views import CategoriasViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriasViewSet)

urlpatterns = router.urls
