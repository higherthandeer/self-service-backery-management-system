from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Customer, SaleReceipt
from apps.system.serializers.CustomerSerializer import CustomerSerializer
from apps.system.serializers.ReceiptSerializer import SaleReceiptSerializer


class MemberViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    @action(detail=False, methods=['get'])
    def get_receipt(self, request, page, limit):
        """获取所有用户信息"""
        customer = request.user.customer
        # serializer_class = SaleReceiptSerializer
        queryset = SaleReceipt.objects.filter(customer=customer)

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

    @action(detail=False, methods=['get'])
    def get_member_info(self, request, *args, **kwargs):
        """获取用户会员信息"""
        try:
            customer = request.user.customer
            if not customer:
                return Response({"code": 203, "message": "找不到会员信息", "data": None, "ok": False})
            serializer = CustomerSerializer(customer)  # 移除 many=True
            return Response({"code": 200, "message": "成功", "data": serializer.data, "ok": True})
        except Customer.DoesNotExist:
            return Response({"code": 203, "message": "找不到会员信息", "data": None, "ok": False})
