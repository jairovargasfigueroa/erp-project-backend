"""
URL configuration for erp_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from erp_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('productos.urls')),
    path('api/', include('categorias.urls')),
    path('api/', include('sucursales.urls')),
    path('api/', include('almacenes.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('ventas.urls')),
    path('api/', include('proveedores.urls')),
    path('api/', include('compras.urls')),
    path('api/', include('movimientosInventario.urls')),  # Incluir las URLs de movimientoInventario
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
