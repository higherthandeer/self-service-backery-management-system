from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from apps.system.serializers.RegisterSerializer import RegisterSerializer


class RegisterViewSet(ModelViewSet):
    """注册视图"""
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """保存前端传入的添加用户数据"""
        data = request.data
        # print(data)
        # 使用序列化器将数据转换为模型实例
        serializer = self.get_serializer(data=data)
        print(serializer)
        result = serializer.is_valid()
        # 如果未通过校验
        if not result:
            username_errors = serializer.errors.get('username')
            error_message = username_errors[0]
            # error_message = ' '.join(serializer.errors.get('non_field_errors', ['Unknown error']))
            return Response({"code": 201, "message": "注册失败具体原因为：" + error_message, "data": None, "ok": False})
        self.perform_create(serializer)
        return Response({"code": 200, "message": "成功", "data": None, "ok": True})
