from rest_framework.pagination import CursorPagination, PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "sahifa o'lchami"
    page_query_param = 'sahifa'
    page_size_query_description = "Har bit sahifada nechtadan bo'lishi mumkin"
    max_page_size = 100
    page_size = 1


class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'
