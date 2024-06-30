from rest_framework import serializers
from apps.system.serializers import CustomerSerializer
from apps.system.models import SaleReceipt, ReceiptItem


class ReceiptItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptItem
        fields = ['breadname', 'price', 'quantity', 'sub_total']


class SaleReceiptSerializer(serializers.ModelSerializer):
    detail = ReceiptItemSerializer(many=True, read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source='customer',
        read_only=True,  # 如果在创建或更新时不需要修改这个字段
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())  # 如果需要默认设置为当前用户（可选）
    )
    discount = serializers.SerializerMethodField()

    class Meta:
        model = SaleReceipt
        fields = ['id', 'date', 'total', 'customer_id', 'discount', 'detail']

    def get_discount(self, obj):
        # 假设Order模型有一个关联到Customer的外键字段叫做customer
        customer = obj.customer
        if not customer:  # 如果是匿名会员则此销售单无会员绑定所以特殊判断
            discount = 10
            return discount
        # 你可以直接在这里实现与CustomerSerializer中相同的逻辑
        discount_obj = customer.get_discount()  # 假设Customer模型有一个get_discount方法
        if discount_obj:
            return discount_obj.discount
        else:
            return None


class SalesPerYearSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

