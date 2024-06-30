from rest_framework import serializers

from apps.system.models import Role
from apps.system.serializers.PermissionSerializer import PermissionSerializer


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    permission = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = Role
        fields = ["id", "name", "permission"]
