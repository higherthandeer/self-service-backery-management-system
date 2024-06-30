from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import User, Role, Customer
from apps.system.serializers.UserSerializer import UserSerializer
from apps.system.serializers.RoleSerializer import RoleSerializer


class UserViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, page, limit):
        """获取所有用户信息"""
        queryset = self.filter_queryset(self.get_queryset())

        # 使用 serializer_class 获取序列化器类
        serializer_class = self.get_serializer_class()
        # 获取序列化字段名给前端table作列名
        columns = []
        for field_name in serializer_class.Meta.fields:
            field = serializer_class.Meta.model._meta.get_field(field_name)
            columns.append({
                'prop': field_name,
                'label': field.verbose_name
            })

        # 使用分页器
        paginator = CustomPagination(request, queryset, UserSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到用户信息", "data": "null", "ok": False})
        serializer = self.get_serializer(queryset, many=True)
        total = len(serializer.data)

        # 取得分页器返回结果
        result = paginator.get_paginated_data()  # 每页数据
        # print()

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
        keyword = self.request.query_params.get('username', None)
        if keyword:
            queryset = queryset.filter(username__icontains=keyword)
            # print(queryset)
        return queryset

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

    def delete_batch(self, request, pk_list):
        """批量删除"""
        id_list = pk_list.split(',')
        try:
            id_list = [int(pk) for pk in id_list]  # 获取要删除的对象的ID列表
            # 执行批量删除操作
            User.objects.filter(pk__in=id_list).delete()
            return Response({'code': 200, 'message': '批量删除成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 500, 'message': '批量删除失败，原因：' + str(e), "data": None, "ok": False})

    @action(detail=True, methods=['get'])
    def get_role(self,  request, *args, **kwargs):
        """获取角色"""
        user = self.get_object()  # 根据用户主键id获取用户对象
        # print(user)
        current_user_roles = user.role.all()  # 获取当前登录用户的所有角色
        all_roles = Role.objects.all()  # 获取角色表中的所有角色
        current_user_roles_serializer = RoleSerializer(current_user_roles, many=True)
        all_roles_serializer = RoleSerializer(all_roles, many=True)
        return Response({
            'code': 200, 'message': '成功',
            "data": {
                'curRoles': current_user_roles_serializer.data,
                'allRolesList': all_roles_serializer.data
            },
            "ok": True
        })

    @action(detail=False, methods=['post'])
    def set_role(self, request):
        """设置角色"""
        user_id = request.data.get('userId')
        role_ids = request.data.get('roleIdList')
        # print(user_id)
        # print(role_id_list)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'code': 201, 'message': '失败！用户不存在', "data": None, "ok": False})

        # 获取当前用户ID对应的所有角色ID
        cur_role_ids = user.role.values_list('id', flat=True)
        # 将当前权角色D列表转换为集合
        cur_role_ids_set = set(cur_role_ids)

        # 将前端传递的角色ID列表转换为集合
        new_role_ids_set = set(role_ids)
        # 计算需要增加的角色ID列表
        add_role_ids = new_role_ids_set - cur_role_ids_set

        # 计算需要删除的角色ID列表
        remove_role_ids = cur_role_ids_set - new_role_ids_set

        # 增加角色
        for role_id in add_role_ids:
            try:
                role = Role.objects.get(id=role_id)
                user.role.add(role)
                if role.name == '顾客':  # 如果角色为顾客则将其插入会员表
                    Customer.objects.create(user=user)

            except role.DoesNotExist:
                return Response({'code': 202, 'message': '失败！角色不存在', "data": None, "ok": False})

        # 删除权限
        for role_id in remove_role_ids:
            try:
                role = Role.objects.get(id=role_id)
                user.role.remove(role)
                if role.name == '顾客':  # 如果角色为顾客则将移出顾客表
                    Customer.objects.filter(user=user).delete()
            except role.DoesNotExist:
                return Response({'code': 202, 'message': '失败！角色不存在', "data": None, "ok": False})

        return Response({'code': 200, 'message': '成功', "data": None, "ok": True})

    @action(detail=False, methods=['post'])
    def reset_pwd(self, request):
        """重置密码"""
        # print(request.data)
        try:
            id = request.data.get('id')
            user = User.objects.get(id=id)
            pwd = '123456'
            user.set_password(pwd)
            user.save()
            return Response({"code": 200, "message": '用户密码重置成功！', "data": None, "ok": True})
        except ObjectDoesNotExist:
            return Response({"code": 201, "message": '用户不存在！', "data": None, "ok": False})


