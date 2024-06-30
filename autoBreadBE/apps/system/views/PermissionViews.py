from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Permission
from apps.system.serializers.PermissionSerializer import PermissionSerializer


class PermissionViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def list(self, request, *args, **kwargs):
        """获取所有权限信息"""
        queryset = self.get_queryset()
        # print(queryset)
        permissions_data = self.get_permissions_tree(queryset)
        return Response({"code": 200, "message": "成功",
                         "data": permissions_data, "ok": True})

    def get_permissions_tree(self, queryset):
        data = []
        permissions = queryset.filter(pid=None)  # 获取顶级权限
        for permission in permissions:
            permission_data = self.serialize_permission(permission)
            data.append(permission_data)
        return data

    def serialize_permission(self, permission):
        permission_data = {
            'id': permission.id,
            'pid': permission.pid_id,
            'name': permission.name,
            'level': permission.level,
            'code': permission.code,
            'children': []
        }
        children = permission.children.all()
        for child in children:
            child_data = self.serialize_permission(child)
            permission_data['children'].append(child_data)
        return permission_data

    def create(self, request, *args, **kwargs):
        """保存前端传入的添加用户数据"""
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
        """删除前端url中id对应的用户数据"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})
