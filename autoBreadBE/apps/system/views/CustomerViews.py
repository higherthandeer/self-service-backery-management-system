from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from autoBreadBE.utils.pagination import CustomPagination
from apps.system.models import Customer, Role
from apps.system.serializers.CustomerSerializer import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request, page, limit):
        """获取所有用户信息"""
        queryset = self.filter_queryset(self.get_queryset())

        # 使用 serializer_class 获取序列化器类
        serializer_class = self.get_serializer_class()
        # 获取序列化字段名给前端table作列名
        columns = [{'prop': 'id', 'label': '会员ID'},
                   {'prop': 'username', 'label': '用户名'},
                   {'prop': 'name', 'label': '真实姓名'},
                   {'prop': 'level', 'label': '会员等级'},
                   {'prop': 'score', 'label': '会员积分'},
                   {'prop': 'discount', 'label': '会员折扣'},
                   ]
        # for field_name in serializer_class.Meta.fields:
        #     field = serializer_class.Meta.model._meta.get_field(field_name)
        #     columns.append({
        #         'prop': field_name,
        #
        #     })

        # 使用分页器
        paginator = CustomPagination(request, queryset, CustomerSerializer, page, limit)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到会员信息", "data": "null", "ok": False})
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
        keyword = self.request.query_params.get('customerId', None)
        if keyword:
            queryset = queryset.filter(id__icontains=keyword)
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
        user = instance.user  # 假设Customer模型有一个user字段关联到User
        role = Role.objects.get(name='顾客')
        user.role.remove(role)   # 用户对应角色字段移除user
        try:
            self.perform_destroy(instance)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})

