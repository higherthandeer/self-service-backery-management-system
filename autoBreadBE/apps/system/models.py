import hashlib
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.system.config import cfg
from apps.system.utils.create_uuid import UUIDTools

# Create your models here.
MEDIA_ADDR = "http://127.0.0.1:8000/media/"


class User(AbstractUser):
    """用户表"""
    # id = models.UUIDField(primary_key=True, auto_created=True, default=UUIDTools.uuid4_hex, editable=False)
    username = models.CharField(max_length=30,
                                unique=True,
                                db_index=True,
                                verbose_name="用户名",
                                help_text="用户名")
    name = models.CharField(max_length=64,
                            null=True,
                            blank=True,
                            verbose_name="真实姓名",
                            help_text="真实姓名")
    gender = models.IntegerField(choices=cfg.GENDER_CHOICES,
                                 default=0,
                                 verbose_name="性别",
                                 null=True,
                                 blank=True,
                                 help_text="性别")
    mobile = models.CharField(max_length=11,
                              verbose_name="手机号码",
                              null=True,
                              blank=True,
                              help_text="手机号码")
    email = models.EmailField(max_length=50,
                              verbose_name="邮箱",
                              null=True,
                              blank=True,
                              help_text="邮箱")
    birthday = models.DateField(verbose_name="生日",
                                null=True,
                                blank=True,
                                help_text="生日")
    avatar = models.ImageField(upload_to='avatar',
                               max_length=255,
                               null=True,
                               blank=True,
                               verbose_name='头像',
                               help_text="头像")
    role = models.ManyToManyField(to="Role",
                                  blank=True,
                                  verbose_name='角色',
                                  help_text="角色",
                                  related_name='users')

        # 对密码加密？

    def set_password(self, raw_password):
        hashed_password = hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest()
        super().set_password(hashed_password)

    def get_avatar_url(self):
        """生成头像URL"""
        return MEDIA_ADDR + str(self.avatar)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username


class Customer(models.Model):
    """会员表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', verbose_name="用户")
    level = models.IntegerField(default=0, verbose_name="会员等级", help_text="会员等级")
    score = models.IntegerField(default=0, verbose_name="会员积分", help_text="会员积分")

    def get_discount(self):
        """
        根据会员等级获取对应的优惠信息（如果有的话）
        """
        try:
            return CustomerLevel.objects.get(level=self.level)
        except CustomerLevel.DoesNotExist:
            return None

    def update_level(self):
        # 遍历所有会员等级，找到当前积分所属的最高等级
        for level in CustomerLevel.objects.all().order_by('-required_score'):  # 按 required_score 升序排序
            if self.score >= level.required_score:
                # 更新会员等级为找到的第一个符合条件的等级
                self.level = level.level
                self.save()
                break  # 找到后退出循环


class CustomerLevel(models.Model):
    """优惠表"""
    level = models.IntegerField(unique=True,
                                db_index=True,
                                verbose_name="会员等级",
                                help_text="会员等级")
    discount = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   verbose_name="优惠折扣",
                                   help_text="优惠折扣")
    required_score = models.IntegerField(default=0,
                                         verbose_name="所需积分",
                                         help_text="所需积分")  # 达到此等级所需的积分


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64,
                            unique=True,
                            verbose_name="角色名称",
                            help_text="角色名称")
    permission = models.ManyToManyField(to="Permission",
                                        verbose_name="权限",
                                        help_text="权限", )


class Permission(models.Model):
    """权限表"""
    pid = models.ForeignKey('self',
                            related_name='children',
                            null=True, blank=True,
                            on_delete=models.CASCADE,
                            verbose_name="父权限id",
                            help_text="父权限id"
                            )
    name = models.CharField(max_length=30,
                            unique=True,
                            verbose_name="权限名称",
                            help_text="权限名称")
    code = models.CharField(max_length=30,
                            unique=True,
                            null=True,
                            verbose_name="权限值",
                            help_text="权限值")
    # tocode = models.CharField(max_length=100,
    #                           verbose_name="权限名称",
    #                           help_text="权限名称")
    is_button = models.BooleanField(default=0,
                                    verbose_name="是否为按钮",
                                    help_text="是否为按钮",)  # 根据实际需求调整类型
    # status = models.NullBooleanField(blank=True,
    #                                  null=True,
    #                                  verbose_name="权限名称",
    #                                  help_text="权限名称")
    level = models.IntegerField(null=True,
                                blank=True,
                                verbose_name="权限等级",
                                help_text="权限等级")
    # select = models.BooleanField(default=False,
    #                              verbose_name="是否选中",
    #                              help_text="是否选中")


class Goods(models.Model):
    """商品表"""
    breadname = models.CharField(max_length=64,
                                 verbose_name="面包名称",
                                 help_text="面包名称")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="单价",
                                help_text="单价")
    MFG_date = models.DateField(verbose_name="生产日期", help_text="生产日期")
    shield_life = models.IntegerField(verbose_name="保质期（天）", help_text="保质期（天）")
    count = models.IntegerField(verbose_name="商品总数", help_text="商品总数")
    sale_count = models.IntegerField(verbose_name="售出数量", help_text="售出数量")
    is_expired = models.BooleanField(default=False, verbose_name="是否过期", help_text="是否过期")

    @property
    def is_expired_now(self):
        """检查商品是否已过期"""
        expiration_date = self.MFG_date + timedelta(days=self.shield_life)
        return expiration_date <= timezone.now().date()


class Inventory(models.Model):
    """库存表"""
    breadname = models.CharField(max_length=64,
                                 verbose_name="面包名称",
                                 help_text="面包名称",)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="进价",
                                help_text="进价")
    MFG_date = models.DateField(verbose_name="生产日期", help_text="生产日期")
    shield_life = models.IntegerField(verbose_name="保质期（天）", help_text="保质期（天）")
    count = models.IntegerField(verbose_name="库存总数", help_text="库存总数")
    out_count = models.IntegerField(verbose_name="出库数量", help_text="出库数量", default=0)
    is_expired = models.BooleanField(default=False, verbose_name="是否过期", help_text="是否过期")
    goods = models.OneToOneField(Goods, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory')

    @property
    def is_expired_now(self):
        """检查商品是否已过期"""
        expiration_date = self.MFG_date + timedelta(days=self.shield_life)
        return expiration_date <= timezone.now().date()


# class StockOrder(models.Model):
#     """进货订单表"""
#     bread_name = models.CharField(max_length=64,
#                                   unique=True,
#                                   verbose_name="面包名称",
#                                   help_text="面包名称")
#     count = models.IntegerField(verbose_name="进货数量", help_text="进货数量")
#     is_finished = models.BooleanField(default=False, verbose_name="是否进货完成", help_text="是否进货完成")
#     start_date = models.DateTimeField(auto_now_add=True, verbose_name="订单创建时间", help_text="订单创建时间")
#     finish_date = models.DateTimeField(null=True,
#                                        auto_now_add=True,
#                                        verbose_name="进货完成时间",
#                                        help_text="进货完成时间")
#     estimate_cost = models.DecimalField(max_digits=10,
#                                         decimal_places=2,
#                                         verbose_name="预计花费",
#                                         help_text="预计花费")
#     actual_cost = models.DecimalField(max_digits=10,
#                                       decimal_places=2,
#                                       verbose_name="实际花费",
#                                       help_text="实际花费")


class SaleReceipt(models.Model):
    """销售单表"""
    date = models.DateTimeField(auto_now_add=True, verbose_name="消费时间", help_text="消费时间")
    total = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="总计花费（元）",
                                help_text="总计花费（元）")
    customer = models.ForeignKey(Customer,
                                 on_delete=models.SET_NULL,  # 当Customer被删除时，将SalesOrder的customer字段设置为NULL
                                 null=True,  # 允许customer字段为空
                                 blank=True,  # 在表单验证中，允许该字段为空（虽然对数据库存储来说不是必需的）
                                 related_name='sale_receipt',
                                 verbose_name="会员"
                                 )


class ReceiptItem(models.Model):
    """销售详情表"""
    receipt = models.ForeignKey(to="SaleReceipt",
                                on_delete=models.PROTECT,
                                verbose_name="销售单",
                                help_text="销售单",
                                related_name="detail")
    breadname = models.CharField(max_length=64,
                                 verbose_name="面包名称",
                                 help_text="面包名称")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="单价",
                                help_text="单价")
    quantity = models.PositiveIntegerField(verbose_name="购买数量", help_text="购买数量")
    sub_total = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    verbose_name="单种商品总价",
                                    help_text="单种商品总价")

    # @property
    # def get_breadname(self):
    #     return self.bread.name
    #
    # @property
    # def get_price(self):
    #     return self.bread.price


class DatabaseBackup(models.Model):
    """数据库备份文件表"""
    backup_name = models.CharField(unique=True, max_length=255, verbose_name="备份名字")
    backup_date = models.DateTimeField(auto_now_add=True, verbose_name="备份时间")
    backup_description = models.TextField(blank=True, verbose_name="备份描述")
    backup_file = models.FileField(upload_to='backups', verbose_name="备份文件")  # 如果你需要存储备份文件