from datetime import timedelta
from decimal import Decimal

from django.forms import DateField
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Goods, ReceiptItem, SaleReceipt, Customer, CustomerLevel
from apps.system.serializers.GoodsSerializer import GoodsSerializer
from apps.system.serializers.ReceiptSerializer import SaleReceiptSerializer
from django.db.models import F, Q, ExpressionWrapper, DurationField


class GoodsViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer

    def list(self, request, page, limit):
        """获取对应页商品信息"""
        # 传入每列列名给前端动态生成table列
        model_fields = self.queryset.model._meta.fields
        columns = [{'prop': field.name, 'label': field.verbose_name} for field in model_fields]

        queryset = self.filter_queryset(self.get_queryset())
        for good in queryset:
            expiration_date = good.MFG_date + timezone.timedelta(days=good.shield_life)
            if expiration_date <= timezone.now().date():  # 比较日期部分
                good.is_expired = True
                good.save()
        # 使用分页器
        paginator = CustomPagination(request, queryset, GoodsSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到商品信息", "data": "null", "ok": False})
        serializer = self.get_serializer(queryset, many=True)
        total = len(serializer.data)

        # 取得分页器返回结果
        result = paginator.get_paginated_data()  # 每页数据

        # 获取当页数据
        page_data = result["data"]
        # 获取总页数
        pages = result["pages"]
        return Response({"code": 200, "message": "成功",
                         "data": {"records": page_data,
                                  "total": total,
                                  "columns": columns,
                                  "size": limit,
                                  "current": page,
                                  "pages": pages}, "ok": True})

    def get_queryset(self):
        queryset = super().get_queryset()
        # 如果请求中包含查询参数，则根据参数进行过滤
        keyword = self.request.query_params.get('breadname', None)
        if keyword:
            queryset = queryset.filter(breadname__icontains=keyword)
            # print(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        """保存前端传入的添加数据"""
        data = request.data
        # print(data)
        # 使用序列化器将数据转换为模型实例
        serializer = self.get_serializer(data=data)
        result = serializer.is_valid()
        # 如果未通过校验
        if not result:
            return Response({"code": 201, "message": "失败", "data": None, "ok": False})
        self.perform_create(serializer)
        return Response({"code": 200, "message": "成功", "data": None, "ok": True})

    def update(self, request, *args, **kwargs):
        """修改前端传入的对象数据并保存到数据库"""
        # 检索要更新的对象
        # print(request.data)
        instance = self.get_object()

        # 序列化要更新的对象，使用请求中的数据
        serializer = self.get_serializer(instance, data=request.data)

        # 验证并保存序列化数据
        result = serializer.is_valid()
        # 如果未通过校验
        if not result:
            return Response({"code": 201, "message": "失败", "data": None, "ok": False})
        serializer.save()
        return Response({"code": 200, "message": "成功", "data": None, "ok": True})

    def destroy(self, request, *args, **kwargs):
        """删除前端url中id对应的商品数据"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})

    @action(detail=False, methods=['post'])
    def sale(self, request, *args, **kwargs):
        """批量售出商品"""
        # print(request.data)
        detect_data = request.data.get('detectData')
        customer_id = request.data.get('customerId')
        discount = 10
        # 用户输入会员ID才会查询会员
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                customer_level = CustomerLevel.objects.get(level=customer.level)  # 使用正确的字段名替换'level_field'
                discount = customer_level.discount
                # print(customer)
            except Exception as e:
                # 如果出现任何异常，回滚事务并返回错误响应，也就是说销毁最开始创建的便于关联的总销售记录
                return Response({'code': 500, 'message': "会员不存在，请重新输入！", 'data': None, 'ok': False})

        # print(detect_data, customer_id)
        total_price = 0
        receipt_items = []
        current_time = timezone.now().isoformat()  # 使用isoformat()方法获取ISO 8601格式的时间字符串

        try:
            with transaction.atomic():  # 使用事务保证操作的原子性
                # 创建总销售记录
                if customer_id:
                    sale_receipt = SaleReceipt.objects.create(total=0, date=current_time, customer=customer)  # 先创建总销售记录以保证正确
                else:
                    sale_receipt = SaleReceipt.objects.create(total=0, date=current_time)

                for item in detect_data:
                    name = item['name']
                    count = item['count']  # 假设售出数量的键名为'sold_quantity'
                    price = item['price']

                    try:
                        # 查询商品
                        # goods = Goods.objects.get(breadname=name, is_expired=False)
                        goods = Goods.objects.filter(breadname=name, is_expired=False).first()
                        # print(goods)
                    except Goods.DoesNotExist:
                        return Response({'code': 404, 'message': f'商品  {name} 不存在', "data": None, "ok": False})

                    # 记录销售详情
                    sub_total = price * count * discount * Decimal(str(0.1))
                    receipt_item = ReceiptItem.objects.create(receipt=sale_receipt,
                                                              breadname=goods.breadname,
                                                              price=goods.price,
                                                              quantity=count,
                                                              sub_total=sub_total)
                    receipt_items.append(receipt_item)

                    goods.sale_count += count  # 售卖数量增加
                    goods.save()
                    if goods.count <= goods.sale_count:  # 商品卖完移除此商品
                        goods.delete()

                    total_price += sub_total
                # 更新总销售记录的总价
                sale_receipt.total = total_price
                sale_receipt.save()
                # 更新顾客积分
                if customer_id:
                    customer.score += total_price
                    # print(customer.score)
                    customer.save()
                    customer.update_level()  # 更新会员等级
        except Exception as e:
            # 如果出现任何异常，回滚事务并返回错误响应，也就是说销毁最开始创建的便于关联的总销售记录
            transaction.rollback()
            return Response({'code': 500, 'message': str(e), 'data': None, 'ok': False})

        return Response({'code': 200, 'message': '商品售出成功', "data": None, "ok": True})

    @action(detail=False, methods=['get'])
    def expiring(self, request, *args, **kwargs):
        # 定义快过期的天数，比如1天
        days_to_expire = 1

        # 使用MySQL的DATE_ADD函数来计算过期日期
        # 注意：这里假设MFG_date是DateField类型，shield_life是IntegerField类型
        queryset = Goods.objects.all()
        expiring_goods = []

        for good in queryset:
            expiration_date = good.MFG_date + timezone.timedelta(days=good.shield_life)
            if days_to_expire and expiration_date - timezone.timedelta(days=days_to_expire) == timezone.now().date() :
                # 注意这里也应该是 datetime 对象的比较，如果 days_to_expire 是以天为单位的话
                # 商品即将在days_to_expire天内过期
                expiring_goods.append(good)

                # 如果有快过期或已过期的商品，返回它们
        serializer = GoodsSerializer(expiring_goods, many=True)

        if expiring_goods:
            return Response(
                {"code": 200, "message": "存在商品还有一天就将过期请尽快处理！",
                 "data": serializer.data, "ok": True})
        else:
            # 如果没有快过期或已过期的商品，返回没有相关商品的提示
            return Response({"code": 201, "message": "无商品快过期", "data": None, "ok": False})


