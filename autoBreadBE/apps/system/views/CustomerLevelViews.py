from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.system.models import CustomerLevel, Customer
from apps.system.serializers.CustomerLevelSerializer import CustomerLevelSerializer


class CustomerLevelViewSet(ModelViewSet):
    # 全局配置了验证因此不必写身份验证
    queryset = CustomerLevel.objects.all().order_by('id')
    serializer_class = CustomerLevelSerializer

    def list(self, request):
        """获取对应页折扣信息"""
        # 传入每列列名给前端动态生成table列
        model_fields = self.queryset.model._meta.fields
        columns = [{'prop': field.name, 'label': field.verbose_name} for field in model_fields]

        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"code": 203, "message": "找不到商品信息", "data": "null", "ok": False})
        serializer = self.get_serializer(queryset, many=True)
        # print(serializer.data)

        return Response({"code": 200,
                         "message": "成功",
                         "data": {"records": serializer.data,
                                  "columns": columns,
                                  },
                         "ok": True})

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

        # for custometer in Customer.objects.all():
        #     custometer.

        # 验证并保存序列化数据
        result = serializer.is_valid()
        # 如果未通过校验
        if not result:
            return Response({"code": 201, "message": "失败", "data": None, "ok": False})
        serializer.save()
        # 会员等级信息发生变化则检查会员等级是否改变
        for custometer in Customer.objects.all():
            custometer.update_level()
        return Response({"code": 200, "message": "成功", "data": None, "ok": True})

    def destroy(self, request, *args, **kwargs):
        """删除前端url中id对应的商品数据"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'code': 200, 'message': '成功', "data": None, "ok": True})
        except Exception as e:
            return Response({'code': 201, 'message': '失败理由为：' + str(e), "data": None, "ok": False})

