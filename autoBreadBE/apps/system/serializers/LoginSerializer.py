from datetime import datetime, timedelta
import hashlib
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.system.models import User

# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import InvalidToken
#
# # def validate_token(token_str):
# #     try:
# #         token = AccessToken(token_str)
# #         # 调用内置的验证方法，如果验证失败会抛出异常
# #         token_payload = token.payload
# #         # 在 payload 中可以访问添加的自定义数据，如用户名、用户 ID 等
# #         username = token_payload.get('username')
# #         user_id = token_payload.get('user_id')
# #         # 在这里可以根据业务逻辑进一步处理
# #         return True, username, user_id
# #     except InvalidToken:
# #         # 验证失败，token 无效
# #         return False, None, None

# 使用示例


class LoginSerializer(serializers.ModelSerializer):
    """
    登录的序列化器:
    # 重写djangorestframework-simplejwt的序列化器
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]
        # read_only_fields = ["id"]

    # 登录数据校验
    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')
        # hash_password = hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        user = authenticate(username=username, password=password)
        # user = User.objects.filter(username=username, password=password).first()
        # print(user)
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        # print(user.username, user.password)
        data['user'] = user
        return data


class LoginTokenSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        # 前置已经做过检验
        user = attrs
        if user:
            # 如果身份验证成功，生成令牌
            refresh = self.get_token(user)
            data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            data['expire'] = refresh.access_token.payload['exp']  # 有效期
            # 用户名
            data['username'] = user.username
            # 手机号
            data['user_id'] = user.id
            return data
        else:
            # 如果身份验证失败，抛出验证错误
            raise serializers.ValidationError('Unable to login with provided credentials.')


class LoginUserSerializer(serializers.ModelSerializer):
    """获取登录用户信息的序列化器"""
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "avatar", "role"]

    def get_avatar(self, obj):
        return obj.get_avatar_url()


class UserCenterSerializer(serializers.ModelSerializer):
    """获取登录用户信息的序列化器"""
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "name", "gender", "mobile", "email", "birthday", "avatar"]
    #
    def get_avatar(self, obj):
        return obj.get_avatar_url()
