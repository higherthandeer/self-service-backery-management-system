from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import ReceiptItem, SaleReceipt
from apps.system.serializers.ReceiptSerializer import SaleReceiptSerializer


class SaleReceiptView(APIView):
    def get(self, request, page, limit):
        # sales = SaleReceipt.objects.all()
        # serializer = SaleReceiptSerializer(sales, many=True)
        # return Response(serializer.data)
        queryset = SaleReceipt.objects.all()

        # 使用分页器
        paginator = CustomPagination(request, queryset, SaleReceiptSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到订单信息", "data": "null", "ok": False})
        serializer = SaleReceiptSerializer(queryset, many=True)
        total = len(serializer.data)

        # 取得分页器返回结果
        result = paginator.get_paginated_data()  # 每页数据
        # print()

        # 获取当页数据
        page_data = result["data"]
        # 获取总页数
        pages = result["pages"]
        return Response({"code": 200, "message": "成功",
                         "data": {"records": page_data,
                                  "total": total,
                                  "size": limit,
                                  "current": page,
                                  "pages": pages}, "ok": True})


# class SaleReceiptDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             sale = SaleReceipt.objects.get(pk=pk)
#         except SaleReceipt.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = SaleReceiptDetailSerializer(sale)
#         return Response(serializer.data)

