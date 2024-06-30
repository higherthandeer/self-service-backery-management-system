from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.system.serializers.LoginSerializer import LoginSerializer, LoginTokenSerializer, LoginUserSerializer, UserCenterSerializer
from apps.system.models import User
from django.core.files.storage import FileSystemStorage


class LoginView(APIView):
    """登录视图"""
    # 登录视图不需要验证
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # return Response({"code": 0, 'error': '校验失败', "detail": serializer.errors})
            # print(serializer.errors)
            user = serializer.validated_data.get('user')
            # print(user)
            token_serializer = LoginTokenSerializer()
            token = token_serializer.validate(user)  # get_token 方法返回 token 字典
            # print(token)
            access_token = token.get('access')  # 从字典中取出token
            refresh_token = token.get('refresh')  # 从字典中取出token
            return Response({"code": 200,
                             'message': "登录成功",
                             'data': access_token,
                             "refresh": refresh_token,
                             "ok": True}, status=status.HTTP_200_OK)
        else:
            error_message = ' '.join(serializer.errors.get('non_field_errors', ['Unknown error']))
            # print(error_message)
            return Response({"code": 201, "message": "登录失败", "data": '校验失败具体原因为: ' + error_message, "ok": False})


class LogoutView(APIView):
    """退出登录视图"""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        return Response({"code": 200, "message": "退出登录成功", "data": "null", "ok": True})


class UserLoginView(APIView):
    """获取当前登录用户信息"""
    def get(self, request):
        queryset = User.objects.filter(username=request.user.username)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到对应用户信息", "data": None, "ok": False})
        # serializer = LoginUserSerilizer(queryset.first())
        user_instance = queryset.first()
        serializer = LoginUserSerializer(user_instance)

        # 获取用户角色和权限信息
        user_roles = user_instance.role.all()
        routes = []
        buttons = []
        for role in user_roles:
            role_permissions = role.permission.all()
            for permission in role_permissions:
                # 添加权限到路由或按钮列表中
                if permission.is_button:
                    buttons.append(permission.code)
                else:
                    routes.append(permission.code)

        # 将角色和权限信息添加到序列化数据中
        serializer_data = serializer.data
        # serializer_data['roles'] = [role.name for role in user_roles]
        serializer_data['routes'] = routes
        serializer_data['buttons'] = buttons
        # print(serializer_data)
        # print(serializer_data)
        return Response({"code": 200, "data": serializer_data, "ok": True})


class UserCenterView(APIView):
    """获取当前登录用户信息"""
    def get(self, request):
        queryset = User.objects.filter(username=request.user.username)
        if not queryset.exists():
            return Response({"code": 203, "message": "找不到对应用户信息", "data": None, "ok": False})
        # serializer = LoginUserSerilizer(queryset.first())
        user_instance = queryset.first()
        serializer = UserCenterSerializer(user_instance)
        # 将角色和权限信息添加到序列化数据中
        serializer_data = serializer.data
        return Response({"code": 200, "data": serializer_data, "ok": True})

    def post(self, request):
        print(request.data)
        key = request.data.get('key')  # 获取修改参数字段
        value = request.data.get('value')  # 获取输入值
        print(key, value)
        user = request.user
        if key == 'Uname': #  修改用户名字段
            if User.objects.filter(username=value).exists():
                return Response({"code": 400, "message": "新的用户名已存在，请重新输入用户名", "data": None, "ok": False},)
                # 修改用户名
            user.username = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "用户名修改成功", "data": None, "ok": True})
        elif key == 'Name':
            user.name = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "姓名修改成功", "data": None, "ok": True})
        elif key == 'Mobile':
            user.mobile = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "手机号码修改成功", "data": None, "ok": True})
        elif key == 'Email':
            user.email = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "邮件修改成功", "data": None, "ok": True})
        elif key == 'Gender':
            user.gender = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "性别修改成功", "data": None, "ok": True})
        elif key == 'Birthday':
            user.birthday = value
            user.save()  # 保存修改
            return Response({"code": 200, "message": "生日修改成功", "data": None, "ok": True})
        return Response({"code": 500, "message": "未知错误", "data": None, "ok": True})

    # return Response({"code": 200, "message": "修改成功", "data": None, "ok": True})


class UserAvatarView(APIView):
    authentication_classes = []
    permission_classes = []
    """存储用户头像视图"""
    def post(self, request):
        """上传头像"""
        try:
            # print('进入上传头像的接口')
            # print(request.data)
            #
            # print('收到的请求={}'.format(request))
            # print('收到的文件是={}'.format(request.FILES))

            avatar = request.FILES.getlist('file')[0]  # 获取头像名称
            # print('收到的头像是={}'.format(avatar))

            username = request.data.get('username')  # 获取用户名
            # print(username)
            # print("获取用户成功")
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response({"code": 201, "message": '用户不存在！', "data": None, "ok": False})

            # 1. 删除原头像

            try:
                user.avatar.delete()
            except Exception as e:
                return Response({"code": 401, "message": '删除源头像失败' + str(e), "data": None, "ok": False})
            # print("删除")

            # 2. 将传来的头像数据，保存到数据库
            try:
                user.avatar = avatar
                user.save()
            except Exception as e:
                return Response({"code": 402, "message": '保存头像失败' + str(e), "data": None, "ok": False})

            # 3. 拼接图片的路径
            avatar_addr = user.get_avatar_url()
            print("获取URL")
            print('返回的图片链接是={}'.format(avatar_addr))

            return Response({"code": 200, "message": '修改成功', "data": {"avatar": avatar_addr}, "ok": True})
        except Exception as e:
            # 打印异常,并且返回异常数据给前端
            Response({"code": 201, "message": '修改失败' + str(e), "data": None, "ok": True})


class UpdatePwdView(APIView):
    def post(self, request):

        try:
            user = request.user
        except ObjectDoesNotExist:
            return Response({"code": 201, "message": '用户不存在！', "data": None, "ok": False})
        username = user.username
        isChecked = request.data.get('isChecked')
        data = request.data.get('data')
        if not isChecked:
            user = authenticate(username=username, password=data)
            if not user:
                return Response({"code": 401, "message": '用户原密码错误，请重新输入！', "data": None, "ok": False})
            else:
                return Response({"code": 200, "message": '用户原密码正确，请输入新密码！', "data": None, "ok": True})
        else:
            user.set_password(data)
            user.save()
            return Response({"code": 200, "message": '用户修改密码成功，请重新登录！', "data": None, "ok": True})

