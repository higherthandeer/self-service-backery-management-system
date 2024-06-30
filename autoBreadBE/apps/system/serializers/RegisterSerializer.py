from rest_framework import serializers
from apps.system.models import User, Role, Customer


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        # 创建用户实例
        user = User.objects.create(**validated_data)

        # 假设'顾客'角色的name字段是'customer'（你需要根据实际情况修改）
        customer_role, created = Role.objects.get_or_create(name='顾客')

        # 为新创建的用户添加'顾客'角色
        user.role.add(customer_role)
        # 由于是顾客插入会员表
        Customer.objects.create(user=user)
        # hash密码
        user.set_password(validated_data['password'])
        user.save()
        return user


        # user = User(**validated_data)
        # user.set_password(validated_data["password"])
        # user.save()
        # return user