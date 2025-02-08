from rest_framework.pagination import PageNumberPagination

class TenNumberPagination(PageNumberPagination):
    page_size = 10