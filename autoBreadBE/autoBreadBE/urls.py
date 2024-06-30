"""
URL configuration for autoBreadBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from django.views.static import serve

from apps.system.views.LoginViews import LoginView, LogoutView, UserLoginView, UserCenterView, UserAvatarView, UpdatePwdView
from apps.system.views.UserViews import UserViewSet
from apps.system.views.GoodsViews import GoodsViewSet
from apps.system.views.RoleViews import RoleViewSet
from apps.system.views.PermissionViews import PermissionViewSet
from apps.system.views.CustomerViews import CustomerViewSet
from apps.system.views.CustomerLevelViews import CustomerLevelViewSet
from apps.system.views.InventoryViews import InventoryViewSet
from apps.system.views.ReceiptViews import SaleReceiptView
from apps.system.views.RegisterView import RegisterViewSet
from apps.system.views.AllInfoViews import AllInfoViewSet
from apps.system.views.DatabaseViews import DatabaseViewSet
from apps.system.views.MemberViews import MemberViewSet
# from apps.system.views.ReceiptViews import SaleReceiptDetailView
from apps.system.views.YoloV5DetectViews import YOLOv5DetectView
from autoBreadBE import settings

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )
system_router = SimpleRouter()
# system_router.register(r'user/info', UserViewSet)
# system_router.register(r'goods', GoodsViewSet)
# system_router.register(r'sell', AllInfoViewSet, basename="all-info")


urlpatterns = [
    path("api-auth/", include('rest_framework.urls')),   # drf登陆退出
    path("admin/", admin.site.urls),
    # 主要以media开头，后面写什么都行
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('api/', include(system_router.urls)),
    # 登录接口
    path("api/login/", LoginView.as_view()),
    # 注册接口
    path("api/register/", RegisterViewSet.as_view({'post': 'create'})),
    # 退出接口
    path("api/logout/", LogoutView.as_view()),
    # 获取当前登录用户信息
    path("api/user/info/", UserLoginView.as_view()),
    path("api/user/center/", UserCenterView.as_view()),
    # 收集用户头像
    path("api/avatar/", UserAvatarView.as_view()),
    # 修改密码
    path("api/update/pwd/", UpdatePwdView.as_view()),

    # 获取商品信息
    path("api/goods/info/<int:page>/<int:limit>/", GoodsViewSet.as_view({'get': 'list'})),
    # 添加商品信息
    path("api/goods/add/", GoodsViewSet.as_view({'post': 'create'})),
    # 修改商品信息
    path("api/goods/update/<int:pk>/", GoodsViewSet.as_view({'put': 'update'})),
    # 删除商品
    path("api/goods/remove/<int:pk>/", GoodsViewSet.as_view({'delete': 'destroy'})),
    # 出售商品
    path("api/goods/sale/", GoodsViewSet.as_view({'post': 'sale'})),
    # 商品过期
    path("api/goods/expire/", GoodsViewSet.as_view({'get': 'expiring'})),

    # 获取全部用户信息
    path("api/acl/user/<int:page>/<int:limit>/", UserViewSet.as_view({'get': 'list'})),
    # 添加用户信息
    path("api/acl/user/add/", UserViewSet.as_view({'post': 'create'})),
    # 修改用户信息
    path("api/acl/user/update/<int:pk>/", UserViewSet.as_view({'put': 'update'})),
    # 删除用户
    path("api/acl/user/remove/<int:pk>/", UserViewSet.as_view({'delete': 'destroy'})),
    # 批量删除用户
    path("api/acl/user/batchRemove/<str:pk_list>/", UserViewSet.as_view({'delete': 'delete_batch'})),
    # 获取用户职位接口
    path("api/acl/user/get/role/<int:pk>/", UserViewSet.as_view({'get': 'get_role'})),
    # 修改用户职位接口
    path("api/acl/user/set/role/", UserViewSet.as_view({'post': 'set_role'})),
    # 重置用户密码
    path("api/acl/user/reset/pwd/", UserViewSet.as_view({'post': 'reset_pwd'})),


    # 获取全部角色信息
    path("api/acl/role/<int:page>/<int:limit>/", RoleViewSet.as_view({'get': 'list'})),
    # 添加角色信息
    path("api/acl/role/add/", RoleViewSet.as_view({'post': 'create'})),
    # 修改角色信息
    path("api/acl/role/update/<int:pk>/", RoleViewSet.as_view({'put': 'update'})),
    # 删除角色
    path("api/acl/role/remove/<int:pk>/", RoleViewSet.as_view({'delete': 'destroy'})),
    # 获取角色对应权限的接口
    path("api/acl/role/get/permission/<int:pk>/", RoleViewSet.as_view({'get': 'get_permission'})),
    # 修改角色对应权限的接口
    path("api/acl/role/set/permission/", RoleViewSet.as_view({'post': 'set_permission'})),


    # 获取所有权限接口
    path("api/acl/permission/", PermissionViewSet.as_view({'get': 'list'})),
    # 添加权限信息
    path("api/acl/permission/add/", PermissionViewSet.as_view({'post': 'create'})),
    # 修改权限信息
    path("api/acl/permission/update/<int:pk>/", PermissionViewSet.as_view({'put': 'update'})),
    # 删除权限
    path("api/acl/permission/remove/<int:pk>/", PermissionViewSet.as_view({'delete': 'destroy'})),

    # 获取全部顾客信息
    path("api/customer/<int:page>/<int:limit>/", CustomerViewSet.as_view({'get': 'list'})),
    # 添加顾客信息
    path("api/customer/add/", CustomerViewSet.as_view({'post': 'create'})),
    # 修改顾客信息
    path("api/customer/update/<int:pk>/", CustomerViewSet.as_view({'put': 'update'})),
    # 删除顾客
    path("api/customer/remove/<int:pk>/", CustomerViewSet.as_view({'delete': 'destroy'})),

    # 获取全部折扣信息
    path("api/discount/", CustomerLevelViewSet.as_view({'get': 'list'})),
    # 添加顾客信息
    path("api/discount/add/", CustomerLevelViewSet.as_view({'post': 'create'})),
    # 修改顾客信息
    path("api/discount/update/<int:pk>/", CustomerLevelViewSet.as_view({'put': 'update'})),
    # 删除顾客
    path("api/discount/remove/<int:pk>/", CustomerLevelViewSet.as_view({'delete': 'destroy'})),


    # 添加库存信息
    path("api/inventory/add/", InventoryViewSet.as_view({'post': 'create'})),
    # 获取库存信息
    path("api/inventory/info/<int:page>/<int:limit>/", InventoryViewSet.as_view({'get': 'list'})),
    # 添加库存信息
    # path("api/goods/add/", GoodsViewSet.as_view({'post': 'create'})),
    # 修改库存信息
    path("api/inventory/update/<int:pk>/", InventoryViewSet.as_view({'put': 'update'})),
    # 出库
    path("api/inventory/remove/<int:pk>/", InventoryViewSet.as_view({'delete': 'destroy'})),
    # 删除库存
    path("api/inventory/out/", InventoryViewSet.as_view({'post': 'out_inv'})),
    # 库存过期
    path("api/inventory/expire/", InventoryViewSet.as_view({'get': 'expiring'})),
    # 库存统计
    path("api/inventory/statistics/header/", InventoryViewSet.as_view({'get': 'statistics_header'})),
    path("api/inventory/statistics/value/", InventoryViewSet.as_view({'get': 'statistics_value'})),
    path("api/inventory/statistics/count/", InventoryViewSet.as_view({'get': 'statistics_count'})),


    # 销售单
    path("api/sell/receipt/info/<int:page>/<int:limit>/", SaleReceiptView.as_view()),


    # 销售统计头部
    path("api/sell/detail/header/", AllInfoViewSet.as_view({'get': 'get_header_data'})),
    # 销售曲线图
    path("api/sell/per/year/", AllInfoViewSet.as_view({'get': 'sell_per_year'})),
    path("api/sell/per/month/<int:year>/", AllInfoViewSet.as_view({'get': 'sell_per_month'})),
    path("api/sell/per/day/<int:year>/<int:month>/", AllInfoViewSet.as_view({'get': 'sell_per_day'})),
    path("api/sell/catagory/", AllInfoViewSet.as_view({'get': 'sell_catagory'})),


    # 数据备份
    path("api/database/<int:page>/<int:limit>/", DatabaseViewSet.as_view({'get': 'list'})),
    # 添加备份信息
    path("api/database/add/", DatabaseViewSet.as_view({'post': 'create'})),
    # 恢复备份信息
    path("api/database/restore/", DatabaseViewSet.as_view({'post': 'restore'})),
    # 删除备份
    path("api/database/remove/<int:pk>/", DatabaseViewSet.as_view({'delete': 'destroy'})),
    # 批量删除备份
    path("api/database/batchRemove/<str:pk_list>/", DatabaseViewSet.as_view({'delete': 'delete_batch'})),

    # 会员消费记录
    path("api/member/receipt/<int:page>/<int:limit>/", MemberViewSet.as_view({'get': 'get_receipt'})),
    path("api/member/info/", MemberViewSet.as_view({'get': 'get_member_info'})),

    # 图像检测
    # path('api/yolov5/detect/', YOLOv5DetectView.as_view())
    # # 获取Token的接口
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # # 刷新Token有效期的接口
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # # 验证Token的有效性
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
urlpatterns += system_router.urls
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
