from rest_framework import serializers

from apps.system.models import User, Customer
from apps.system.serializers.UserSerializer import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["id", "username", "name", "level", "score", "discount"]

    def get_discount(self, obj):
        # 调用模型的get_discount方法
        discount_obj = obj.get_discount()
        if discount_obj:
            # 如果存在折扣，则序列化折扣对象
            return discount_obj.discount
        else:
            # 如果没有折扣，返回一个空字典或None，或者其他你想要的默认值
            return None
