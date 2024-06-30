# """
# drf认证功能
# """
# from django.conf import settings
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# import jwt
# from jwt import exceptions
#
# class JwtQueryParamsAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         """
#         获取token并判断token的合法性
#         1.切割
#         2.揭秘第二段/判断过期
#         3.验证第三段合法性
#         """
#         token = request.query_params.get('token')
#         salt = settings.SECRET_KEY
#         payload = None
#         msg = None
#         try:
#             payload = jwt.decode(token, salt, algorithms="HS256")
#         except exceptions.ExpiredSignatureError:
#             raise AuthenticationFailed({'code': 1003, 'error': "token已失效"})
#         except jwt.DecodeError:
#             raise AuthenticationFailed({'code': 1003, 'error': "token认证失败"})
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed({'code': 1003, 'error': "非法的token"})
#         # 认证若通过,request.user即payload, request.auth即token
#         return (payload, token)