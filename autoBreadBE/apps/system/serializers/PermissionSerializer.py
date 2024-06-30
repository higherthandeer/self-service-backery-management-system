from rest_framework import serializers

from apps.system.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['id', 'pid', 'name', 'code', 'level', 'children']

    def get_children(self, obj):
        # 递归调用此方法以获取子权限
        children = obj.children.all()
        if children:
            serializer = self.__class__(children, many=True)
            return serializer.data
        return None
