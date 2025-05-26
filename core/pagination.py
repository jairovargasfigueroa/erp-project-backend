from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # valor por defecto
    page_size_query_param = 'page_size'  # permite ?page_size=10
    max_page_size = 100  # por seguridad
