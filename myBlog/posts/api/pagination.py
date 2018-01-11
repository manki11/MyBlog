from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

class PostLimitPagePagination(PageNumberPagination):
    page_size = 10
