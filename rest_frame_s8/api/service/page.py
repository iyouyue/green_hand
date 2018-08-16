from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

# class MyPageNumberPagination(PageNumberPagination):
#     page_size=1
#     page_query_param="page_num"
#     page_size_query_param="size"
#     max_page_size=5

# class MyPageNumberPagination(LimitOffsetPagination):pass

class MyPageNumberPagination(CursorPagination):
    cursor_query_param="page"
    page_size=2
    ordering="id"

