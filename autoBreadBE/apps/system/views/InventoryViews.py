from collections import defaultdict
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DateTimeField, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Inventory, Goods
from apps.system.serializers.InventorySerializer import InventorySerializer


class InventoryViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = Inventory.objects.all().order_by('id')
    serializer_class = InventorySerializer

    def list(self, request, page, limit):
        """获取对应页库存信息"""
        # 传入每列列名给前端动态生成table列
        model_fields = self.queryset.model._meta.fields
        columns = [{'prop': field.name, 'label': field.verbose_name} for field in model_fields]

        queryset = self.filter_queryset(self.get_queryset())

        # 过期字段的筛选
        for inv in queryset:
            expiration_date = inv.MFG_date + timezone.timedelta(days=inv.shield_life)
            if expiration_date <= timezone.now().date():  # 比较日期部分
                inv.is_expired = True
                inv.save()

        # 使用分页器
        paginator = CustomPagination(request, queryset, InventorySerializer, page, limit)
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
        # if(request.data):

        data_list = request.data
        # 没有检测到物体
        if not len(data_list):
            return Response({"code": 201, "message": "失败，没有检测到物体，请重新检测", "data": None, "ok": False})

        dict = defaultdict(list)  # 创建字典分组

        for data in data_list:
            key = (data['name'], data['MFG_date'])
            dict[key].append(data)

        # 遍历分组后的数据
        for key, group in dict.items():
            name, date = key
            total_count = 0
            # 计算当前批次商品检测总个数
            for data in group:
                total_count += data['count']
            price = group[0]['price']
            day = group[0]['shield_life']

            try:
                # 尝试从数据库中获取现有记录
                inventory_obj = Inventory.objects.get(breadname=name, MFG_date=date)
                inventory_obj.count += total_count
                inventory_obj.save()
            except Inventory.DoesNotExist:
                # 如果不存在，创建新的记录
                inventory_obj = Inventory(breadname=name, MFG_date=date, count=total_count, price=price, shield_life=day)
                inventory_obj.save()
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
    def out_inv(self, request, *args, **kwargs):
        data = request.data
        print(request.data)
        new_out = data['new_out']
        inv_count = data['count']
        out_count = data['out_count']
        sale_price = data['sale_price']
        if new_out > inv_count - out_count:
            return Response({'code': 300, 'message': '请重新输入，出库数量不能大于当前库存总数！', "data": None, "ok": False})
        # 尝试获取Goods对象，如果不存在则创建
        inv_id = request.data.get('id')
        goods_id = request.data.get('goods')
        # print(goods_id)
        inv = Inventory.objects.get(id=inv_id)
        try:
            goods = Goods.objects.get(id=goods_id) # 如果存在此种商品
            # print(goods)
            goods.count += new_out  # 出库商品数量加
            goods.save()
            inv.out_count += new_out  # 当前库存数据改变
            inv.save()
            if inv_count == inv.out_count:
                inv.delete()

        except Goods.DoesNotExist:
            goods = Goods.objects.create(
                breadname=data['breadname'],
                price=sale_price,
                MFG_date=data['MFG_date'],
                shield_life=data['shield_life'],
                count=data['new_out'],
                sale_count=0,
                is_expired=data['is_expired'],
                # 其他Goods模型需要的字段...
            )
            inv.goods = goods
            inv.out_count += new_out  # 当前库存数据改变
            inv.save()
            if inv_count == inv.out_count:
                inv.delete()
        return Response({'code': 200, 'message': '成功', "data": None, "ok": True})

    @action(detail=False, methods=['get'])
    def expiring(self, request, *args, **kwargs):
        # 定义快过期的天数，比如1天
        days_to_expire = 1

        # 使用MySQL的DATE_ADD函数来计算过期日期
        # 注意：这里假设MFG_date是DateField类型，shield_life是IntegerField类型
        queryset = Inventory.objects.all()
        expiring_goods = []

        for inv in queryset:
            expiration_date = inv.MFG_date + timezone.timedelta(days=inv.shield_life)
            if days_to_expire and expiration_date - timezone.timedelta(days=days_to_expire) == timezone.now().date():
                # 注意这里也应该是 datetime 对象的比较，如果 days_to_expire 是以天为单位的话
                # 商品即将在days_to_expire天内过期
                expiring_goods.append(inv)

                # 如果有快过期或已过期的商品，返回它们
        serializer = InventorySerializer(expiring_goods, many=True)

        if expiring_goods:
            return Response(
                {"code": 200, "message": "存在库存还有一天就将过期请尽快处理！",
                 "data": serializer.data, "ok": True})
        else:
            # 如果没有快过期或已过期的商品，返回没有相关商品的提示
            return Response({"code": 201, "message": "无库存快过期", "data": None, "ok": False})

    @action(detail=False, methods=['get'])
    def statistics_header(self, request):
        total_count = Inventory.objects.all().aggregate(total_count=Sum('count'))
        total_out = Inventory.objects.all().aggregate(total_out=Sum('out_count'))
        total_value = Inventory.objects.all().aggregate(total_value=Sum(F('count') * F('price')))
        total_loss = Inventory.objects.filter(is_expired=True).aggregate(
            total_loss=Sum(F('price') *(F('count') - F('out_count')))
        )
        # print(total_loss)
        result = {'total_count': total_count.get('total_count'),
                  'total_out': total_out.get('total_out'),
                  'total_value': total_value.get('total_value'),
                  'total_loss': total_loss.get('total_loss')}
        return Response({'code': 200, 'message': '获取信息成功', "data": result, "ok": True})

    @action(detail=False, methods=['get'])
    def statistics_value(self, request):

        # 计算每种面包的进价总和
        bread_price_sums = Inventory.objects.values('breadname') \
            .annotate(value=Sum(F('price') * F('count'))) \
            .order_by('breadname')

        expired_bread_losses = Inventory.objects.filter(is_expired=True) \
            .values('breadname') \
            .annotate(loss=Sum((F('count') - F('out_count')) * F('price'))) \
            .order_by('breadname')

        all_loss = [{'breadname': '三明治', 'loss': 0},
                    {'breadname': '千层蛋糕', 'loss': 0},
                    {'breadname': '法棍', 'loss': 0},
                    {'breadname': '牛角包', 'loss': 0},
                    {'breadname': '甜甜圈', 'loss': 0}]
        # 将all_cate转换为面包名字到损失的字典

        expired_losses_dict = {item['breadname']: item['loss'] for item in expired_bread_losses }

        # 遍历all_cate列表，更新损失值
        for item in all_loss:
            breadname = item['breadname']
            if breadname in expired_losses_dict:
                item['loss'] = expired_losses_dict[breadname]

                # 打印更新后的字典
        result = {'value': bread_price_sums , 'loss': all_loss}
        return Response({'code': 200, 'message': '获取信息成功', "data": result, "ok": True})

    @action(detail=False, methods=['get'])
    def statistics_count(self, request):
        # 按面包名分组，并计算每个面包的库存总数
        cate_counts = []
        inventory_stats = Inventory.objects.values('breadname') \
            .annotate(total=Sum('count')) \
            .order_by('breadname')
        for item in inventory_stats:
            breadname = item['breadname']
            total = item['total']
            cate_counts.append({'name': breadname, 'value': total})
        return Response({'code': 200, 'message': '获取信息成功', "data": cate_counts, "ok": True})
