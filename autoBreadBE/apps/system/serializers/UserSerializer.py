from rest_framework import serializers

from apps.system.models import User
from apps.system.serializers.RoleSerializer import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "name", "password", "gender", "mobile", "email", "birthday", "role"]

    def create(self, validated_data):
        user = User(**validated_data)
        # print(validated_data["password"])
        user.set_password(validated_data["password"])
        # print(user.password)
        user.save()
        return user
