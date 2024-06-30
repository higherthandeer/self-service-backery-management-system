from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.forms import DecimalField
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import calendar

from collections import defaultdict

from apps.system import models
from apps.system.models import User, Inventory, ReceiptItem, SaleReceipt, Goods
from apps.system.serializers.ReceiptSerializer import SaleReceiptSerializer, SalesPerYearSerializer
from django.db.models import Sum, F, ExpressionWrapper, OuterRef, Subquery,DecimalField
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, Coalesce


# from decimal import Decimal


class AllInfoViewSet(ModelViewSet):
    queryset = SaleReceipt.objects.all()
    serializer_class = SaleReceiptSerializer

    @action(detail=False, methods=['get'])
    def get_header_data(self, request):
        user_counts = User.objects.count()
        sale_counts = 0
        profit = 0
        receipt_item = ReceiptItem.objects.all()

        goods = defaultdict(lambda: {'quantity': 0, 'sub_total': 0})
        for obj in receipt_item:
            breadname = obj.breadname
            # 更新商品的总卖出数量和总收入
            goods[breadname]['quantity'] += obj.quantity
            goods[breadname]['sub_total'] += obj.sub_total

        # 将defaultdict转换为普通的dict
        goods = dict(goods)
        for key, value in goods.items():
            # print(value)
            sale_counts += value['quantity']
            profit += value['sub_total']

        # 计算增长率

        today = now().date()

        # 获取上个月的日期
        first_day_of_this_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        # 统计本月和上个月的销售总额
        this_month_total = \
        SaleReceipt.objects.filter(date__month=today.month, date__year=today.year).aggregate(total=Sum('total'))['total'] or 0
        last_month_total = \
        SaleReceipt.objects.filter(date__month=last_day_of_last_month.month, date__year=last_day_of_last_month.year).aggregate(
            total=Sum('total'))['total'] or 0

        # 计算增长额
        growth =this_month_total - last_month_total
        # 计算增长率，确保结果是浮点数
        if last_month_total > 0:
            growth_rate = round(float((Decimal(growth) / Decimal(last_month_total)) * 100), 2)
        else:
            growth_rate = float('inf')  # 如果上个月的总额为零，则增长率为无限大
        return Response({"code": 200, "message": "成功",
                             "data": {"userCounts": user_counts,
                                      "saleCounts": sale_counts,
                                      "profit": profit,
                                      "growth_rate": growth_rate,
                                      "goods": goods,
                                      }, "ok": True})

    @action(detail=False, methods=['get'])
    def sell_per_year(self, request):

        years = SaleReceipt.objects.annotate(year=ExtractYear('date')) \
            .values('year') \
            .annotate(
            total=Sum('total')) \
            .order_by('year')
        serializer = SalesPerYearSerializer(years, many=True)  # 注意：这里可能需要自定义序列化器来处理annotate结果
        # print(serializer.data)
        return Response({"code": 200, "message": "成功", "data": serializer.data, "ok": True})

    @action(detail=False, methods=['get'])
    def sell_per_month(self, request, year):
        # 获取年份的起始和结束日期
        start_date = datetime(year=int(year), month=1, day=1)
        end_date = datetime(year=int(year), month=12, day=31)

        # 使用defaultdict来存储每个月的销售额，初始化为0
        sales_by_month = defaultdict(Decimal)

        # 遍历查询集中的每个销售记录
        for sale in SaleReceipt.objects.filter(date__range=(start_date, end_date)):
            # 获取月份并更新销售额
            month = sale.date.month
            sales_by_month[month] += sale.total

            # 生成包含每个月销售额的列表，如果某个月没有销售额，则显示为0
        result = [{'month': month, 'total': sales_by_month[month]} for month in range(1, 13)]

        return Response({"code": 200, "message": "成功", "data": result, "ok": True})

    @action(detail=False, methods=['get'])
    def sell_per_day(self, request, year, month):
        # 验证输入的月份是否为有效月份
        _, days_in_month = calendar.monthrange(int(year), month)  # 使用calendar模块来获取天数
        start_date = datetime(year=int(year), month=month, day=1)
        end_date = start_date + timedelta(days=days_in_month - 1)

        # 使用defaultdict来存储每天的销售额，初始化为0
        sales_by_day = defaultdict(Decimal)

        # 遍历查询集中的每个销售记录
        for sale in SaleReceipt.objects.filter(date__range=(start_date, end_date)):
            # 获取日期（天）并更新销售额
            day = sale.date.day
            sales_by_day[day] += sale.total

            # 生成包含每天销售额的列表，如果某一天没有销售额，则不包含在列表中
        # 如果需要包含所有天，则需要初始化一个包含所有天的列表，并填充销售额
        # result = [{'day': day, 'total': sales_by_day[day]} for day in sales_by_day]
        # 如果需要包含当月所有天（包括没有销售额的天），请按照下面的方式操作
        result = [{'day': day, 'total': sales_by_day.get(day, Decimal('0'))} for day in
                             range(1, days_in_month + 1)]
        return Response({"code": 200, "message": "成功", "data": result, "ok": True})

    @action(detail=False, methods=['get'])
    def sell_catagory(self, request):
        # 创建一个字典来存储每种面包的进价
        price_dict = {item.breadname: item.price for item in Inventory.objects.all()}
        # print(price_dict)

        # 从ReceiptItem模型中获取每种面包的销售总价和数量
        sales_data = ReceiptItem.objects.values('breadname') \
            .annotate(total_sales=Sum(F('price') * F('quantity')), total_quantity=Sum('quantity')) \
            .order_by('breadname')
        # print(sales_data)
        # 计算利润并存储结果
        profit_data = []
        for item in sales_data:
            breadname = item['breadname']
            total_sales = item['total_sales']
            total_quantity = item['total_quantity']  # 这里假设我们直接使用每行的quantity，而不是Sum
            cost_price = price_dict.get(breadname, 0)
            cost = cost_price * total_quantity  # 使用每行的quantity而不是Sum，因为我们已经按breadname分组
            profit = total_sales - cost
            profit_data.append({'name': breadname, 'value': profit})

            # 返回响应
        return Response({"code": 200, "message": "成功", "data": profit_data, "ok": True})