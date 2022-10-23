from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

SEX_CHOICES = (
    (0, "男"),
    (1, "女"),
)
RW_CHOICES = (
    (0, "回访"),
    (1, "投诉"),
)
STATUS_CHOICES = (
    (0, '已创建'),
    (1, '已付款'),
    (2, '已完成')
)
FSTATUS_CHOICES = (
    (0, '已提交'),
    (1, '已完成')
)
OPERATION_TYPE = (
    ("success", "Create"),
    ("warning", "Update"),
    ("danger", "Delete"),
    ("info", 'Close')
)
VIP = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, '3'),
    (4, '4')
)


class FactoryModel(models.Model):
    name = models.CharField(verbose_name='工厂名', max_length=100, blank=False)
    address = models.CharField(verbose_name='地址', max_length=100, blank=False)
    phone = models.CharField(verbose_name='联系电话', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'factory'
        verbose_name = '工厂信息'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('factory_list')


class GoodsModel(models.Model):
    name = models.CharField(verbose_name='商品名称', max_length=100, blank=False)
    price = models.FloatField(verbose_name='价格')
    factory = models.CharField(verbose_name='工厂', max_length=20)
    types = models.CharField(verbose_name='类别', max_length=100)
    brand = models.CharField(verbose_name='品牌', max_length=100)
    specs = models.CharField(verbose_name='规格', max_length=100)
    color = models.CharField(verbose_name='颜色', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'goods'
        verbose_name = '商品信息'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('good_list')

    @property
    def get_vip_price(self, discounts: float):
        return self.price * discounts


class CustomerModel(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=100, blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES, verbose_name='性别')
    phone = models.CharField(verbose_name='电话', max_length=20, blank=True, null=True)
    birthdate = models.DateTimeField(verbose_name='生日', blank=True, null=True, default=timezone.now)
    address = models.CharField(verbose_name='地址', max_length=100, blank=True, null=True)
    vip_level = models.IntegerField(choices=VIP, verbose_name='VIP等级', blank=True, null=True)

    class Meta:
        db_table = 'customer'
        verbose_name = '客户信息'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customer_list')


class Profile(models.Model):
    name = models.OneToOneField(User, null=True, on_delete=models.CASCADE, verbose_name='用户名')
    namex = models.CharField(max_length=30, blank=True, verbose_name='姓名')
    phone_number = models.CharField(max_length=30, blank=True, verbose_name='电话号码')
    email = models.EmailField(max_length=50, blank=True, verbose_name='电子邮件')
    job = models.CharField(verbose_name='职位', max_length=20, blank=True, null=True)
    base_pay = models.FloatField(verbose_name='基础工资', blank=True, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES, verbose_name='性别')

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')


class UserActivity(models.Model):
    created_by = models.CharField(default="", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    operation_type = models.CharField(choices=OPERATION_TYPE, default="success", max_length=20)
    target_model = models.CharField(default="", max_length=20)
    detail = models.CharField(default="", max_length=50)

    def get_absolute_url(self):
        return reverse('user_activity_list')


class CustomerIndent(models.Model):
    customer = models.CharField(verbose_name='顾客', max_length=20)
    good = models.CharField(verbose_name='商品', max_length=20)
    employees = models.CharField(verbose_name='员工', max_length=20)
    number = models.IntegerField(verbose_name='数量')
    track_num = models.CharField(verbose_name='快递单号', max_length=20, blank=True, null=True)
    income = models.FloatField(verbose_name='收款金额', null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name='订单状态')

    class Meta:
        db_table = 'indent_customer'
        verbose_name = '客户订单'

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('customer_indent_list')


class FactoryIndent(models.Model):
    good = models.CharField(verbose_name='商品', max_length=20)
    employees = models.CharField(verbose_name='员工', max_length=20)
    factory = models.CharField(verbose_name='工厂', max_length=20)
    payment_id = models.CharField(verbose_name='付款单号', max_length=20)
    numbers = models.IntegerField(verbose_name='数量')

    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=FSTATUS_CHOICES, verbose_name='订单状态', default=0)

    class Meta:
        db_table = 'indent_Factory'
        verbose_name = '工厂订单'

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('record_list_fac')


class FeedBackIndent(models.Model):
    customer_indent = models.CharField(verbose_name='顾客订单', max_length=20)
    employees = models.CharField(verbose_name='员工', max_length=20)
    text = models.CharField(verbose_name='反馈内容', max_length=300)

    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=RW_CHOICES, verbose_name='状态')

    class Meta:
        db_table = 'indent_feedback'
        verbose_name = '售后反馈单'

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('record_list_fed')
