import hashlib
# import logging

from django.contrib.auth import get_user_model
# from apps.system.models import User
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

# logger = logging.getLogger(__name__)
UserModel = get_user_model()
class CustomBackend(ModelBackend):
    """
    Django原生认证方式
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # msg = '%s 正在使用本地登录...' % username
        # logger.info(msg)
        # print("auth")
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            check_password = user.check_password(password)
            # print("auth  check" + str(check_password))
            # print(check_password)
            if not check_password:
                check_password = user.check_password(
                    hashlib.md5(password.encode(encoding='UTF-8')).hexdigest())
            if check_password and self.user_can_authenticate(user):
                # print("auth  " + str(self.user_can_authenticate(user)))
                user.last_login = timezone.now()
                user.save()
                return user
