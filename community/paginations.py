from rest_framework.pagination import PageNumberPagination

class ComPostPagination(PageNumberPagination):
    page_size = 7