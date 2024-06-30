from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """自定义分页器，传入page：第几页, limit: 每页数据量来使用"""
    def __init__(self, request, queryset, serializer_class, page, limit):
        self.request = request
        self.queryset = queryset
        self.serializer_class = serializer_class
        self.page = page
        self.limit = limit

    def paginate_queryset(self, queryset, request, page=None):
        self.page_size = self.limit
        self.paginator = self.django_paginator_class(queryset, self.page_size)
        return self.paginator.page(page).object_list

    def get_paginated_data(self):
        self.page_size = self.limit
        page_data = self.paginate_queryset(self.queryset, self.request, page=self.page)
        if not page_data:
            return Response({"code": 203, "message": "找不到商品信息", "data": "null", "ok": False})
        serializer = self.serializer_class(page_data, many=True)

        # 计算总页数
        total_pages = self.paginator.num_pages
        return {"data": serializer.data, "pages": total_pages}
