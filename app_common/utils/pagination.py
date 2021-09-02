from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    # 每页显示多少条
    page_size = 5
    # 最大页数不超过20
    max_page_size = 20
    # 可以通过传入?page=2&size=4，改变默认每页显示的个数
    page_size_query_param = "size"
    # 获取页码数
    page_query_param = "page"
