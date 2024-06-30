from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Role, Permission
from apps.system.serializers.RoleSerializer import RoleSerializer
from apps.system.serializers.PermissionSerializer import PermissionSerializer


class RoleViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer

    def list(self, request, page, limit):
        """获取所有角色信息"""
        # 传入每列列名给前端动态生成table列
        model_fields = self.queryset.model._meta.fields
        columns = [{'prop': field.name, 'label': field.verbose_name} for field in model_fields if field.name in ['id', 'name']]

        queryset = self.filter_queryset(self.get_queryset())

        # 使用分页器
        paginator = CustomPagination(request, queryset, RoleSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到角色信息", "data": "null", "ok": False})
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
        """自定义获取信息为满足根据关键字查询需求"""
        queryset = super().get_queryset()
        # 如果请求中包含查询参数，则根据参数进行过滤
        keyword = self.request.query_params.get('rolename', None)
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
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
        """删除前端url中id对应的角色数据"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})

    @action(detail=True, methods=['get'])
    def get_permission(self, request, *args, **kwargs):
        """获取权限"""
        role_id = kwargs.get('pk')  # 获取角色id
        if role_id is None:
            return Response({'code': 400, 'message': '未提供角色id', 'ok': False})

        try:
            role = Role.objects.get(id=role_id)  # 根据角色id获取角色对象
        except Role.DoesNotExist:
            return Response({'code': 404, 'message': '角色不存在', 'ok': False})
        permissions = Permission.objects.filter(pid=None)  # 获取所有顶级权限

        data = self.serialize_permissions(permissions, role)

        return Response({'code': 200, 'message': '成功', 'data': data, 'ok': True})

    def serialize_permissions(self, permissions, role):
        data = []
        for permission in permissions:
            permission_data = self.serialize_permission(permission, role, set())
            data.append(permission_data)
        return data

    def serialize_permission(self, permission, role, visited):
        permission_data = {
            'id': permission.id,
            'name': permission.name,
            'select': role.permission.filter(id=permission.id).exists()
        }
        children = permission.children.all()
        permission_data['children'] = [self.serialize_permission(child, role, visited) for child in children]

        if permission_data['select']:
            self.set_parent_select(permission, role, visited)

        return permission_data

    def set_parent_select(self, permission, role, visited):
        parent_permission = permission.pid
        if parent_permission and parent_permission.id not in visited:
            visited.add(parent_permission.id)
            if not role.permission.filter(id=parent_permission.id).exists():
                role.permission.add(parent_permission)
                role.save()

            self.set_parent_select(parent_permission, role, visited)

#     permissions = Permission.objects.filter(pid=None)  # 获取所有权限数据
    #     # print(permissions)
    #     data = self.serialize_permissions(permissions, role)
    #     return Response({'code': 200, 'message': '成功', 'data': data, 'ok': True})
    #
    # def serialize_permissions(self, permissions, role):
    #     data = []
    #     for permission in permissions:
    #         permission_data = self.serialize_permission(permission, role)
    #         data.append(permission_data)
    #     return data
    #
    # def serialize_permission(self, permission, role):
    #     permission_data = {
    #         'id': permission.id,
    #         'name': permission.name,
    #         'select': role.permission.filter(id=permission.id).exists()  # 根据角色是否拥有权限来设置select字段
    #     }
    #     children = permission.children.all()
    #     # 递归处理子节点
    #     permission_data['children'] = [self.serialize_permission(child, role) for child in children]
    #     # 如果父节点的select为True，则将所有子节点的select设置为True
    #     if permission_data['select']:
    #         self.set_children_select(permission_data['children'])
    #     return permission_data
    #
    # def set_children_select(self, children):
    #     for child_data in children:
    #         child_data['select'] = True
    #         if 'children' in child_data:
    #             self.set_children_select(child_data['children'])
    #
    @action(detail=False, methods=['post'])
    def set_permission(self, request):
        """设置角色对应权限"""
        role_id = request.data.get('roleId')
        permission_ids = request.data.get('permissionId')
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({'code': 201, 'message': '失败！角色不存在', "data": None, "ok": False})
            # 获取当前角色ID对应的所有权限ID列表
        current_permission_ids = role.permission.values_list('id', flat=True)

        # 将当前权限ID列表转换为集合
        current_permission_ids_set = set(current_permission_ids)

        # 将前端传递的权限ID列表转换为集合
        new_permission_ids_set = set(permission_ids)
        # 计算需要增加的权限ID列表
        add_permission_ids = new_permission_ids_set - current_permission_ids_set

        # 计算需要删除的权限ID列表
        remove_permission_ids = current_permission_ids_set - new_permission_ids_set

        # 增加权限
        for permission_id in add_permission_ids:
            try:
                permission = Permission.objects.get(id=permission_id)
                role.permission.add(permission)
            except Permission.DoesNotExist:
                return Response({'code': 202, 'message': '失败！权限不存在', "data": None, "ok": False})

        # 删除权限
        for permission_id in remove_permission_ids:
            try:
                permission = Permission.objects.get(id=permission_id)
                role.permission.remove(permission)
            except Permission.DoesNotExist:
                return Response({'code': 202, 'message': '失败！权限不存在', "data": None, "ok": False})

        return Response({'code': 200, 'message': '成功', "data": None, "ok": True})