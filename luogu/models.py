import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.


class Customer(models.Model):  # 客户
    user = models.OneToOneField(User, models.CASCADE)  # 密码
    # customer_id = models.IntegerField('客户id', primary_key=True, unique=True)
    user_name = models.CharField('用户名称', max_length=32, null=False, blank=False, default="")  # 用户名称
    telephone = models.CharField('联系方式', max_length=32, null=False, blank=False, default="")  # 联系方式
    consumption_amount = models.FloatField('消费金额', null=False, blank=False, default=0)  # 消费金额
    address = models.CharField('地址', max_length=256, null=False, blank=False, default="")  # 地址
    types = models.CharField('类型', max_length=20, null=False, blank=False, default="")  # 类型
    contact_person = models.CharField('联系人', max_length=32, null=False, blank=False, default="")  # 联系人
    total_shopping_cart = models.FloatField('购物车金额', null=False, blank=False, default=0)  # 购物车金额
    customer_level = models.IntegerField('客户等级', null=False, blank=False, default=0)  # 客户等级
    def __str__(self):
        return self.user_name

    class Meta:
        # 定义后台表显示名称
        verbose_name = '客户管理'
        verbose_name_plural = '客户管理'


class Commodity(models.Model):  # 商品
    # commodity_id = models.IntegerField('商品id', primary_key=True, unique=True)
    stock = models.IntegerField('库存', null=False, blank=False, default=0)  # 库存
    name = models.CharField('商品名称', max_length=256, null=False, blank=False, default="")  # 商品名称
    purchase_price = models.FloatField('进货价', null=False, blank=False, default=0)  # 进货价
    selling_price = models.FloatField('售价', null=False, blank=False, default=0)  # 售价
    sales = models.IntegerField('销量', null=False, blank=False, default=0)  # 销量
    origin_address = models.CharField('产地', max_length=256, null=False, blank=False, default="")  # 产地
    production_date = models.DateField('生产日期')  # 生产日期
    shelf_life = models.DateField('保质期')  # 保质期
    standard = models.IntegerField('规格', null=False, blank=False, default=0)  # 规格单位ml
    detail = models.CharField('商品详情', max_length=256, null=False, blank=False, default="")  # 商品详情
    img = models.ImageField(upload_to='luogu/commodity_img/', verbose_name='商品图片', blank=True, null=True)  # 商品图片
    def __str__(self):
        return str(self.id) + ' ' + self.name

    def upload_img(self):
        try:
            img = mark_safe('<img src="/media/%s" height="100" width="100" />' % (self.img,))
        except:
            img = ''
        return img

    upload_img.short_description = '缩略图'
    upload_img.allows_tags = True

    class Meta:
        # 定义后台表显示名称
        verbose_name = '商品管理'
        verbose_name_plural = '商品管理'

    def get_list_display_links(self, request, list_display):
        if self.list_display_links or not list_display:
            return self.list_display_links
        else:
            return list(list_display)[:1]


class Staff(models.Model):  # 员工
    user = models.OneToOneField(User, models.CASCADE)  # 密码
    # staff_id = models.IntegerField('员工id', primary_key=True, unique=True)  # 员工id
    staff_name = models.CharField('员工名称', max_length=32, null=False, blank=False)  # 员工名称
    telephone = models.CharField('联系方式', max_length=20, null=False, blank=False)  # 联系方式
    gender = models.CharField('性别', max_length=20, default="unknown")  # 性别
    address = models.CharField('家庭地址', max_length=255)  # 家庭地址
    position = models.CharField('职位', max_length=20, null=False, blank=False, default="Employee")  # 职位
    salary = models.IntegerField('薪资', null=False, blank=False, default=0)  # 薪资
    entry_date = models.DateField('入职日期')  # 入职日期
    resignation_date = models.DateField('离职日期', blank=True)  # 离职日期
    birthday = models.DateField('生日')  # 生日
    def __str__(self):
        return self.staff_name

    class Meta:
        # 定义后台表显示名称
        verbose_name = '员工管理'
        verbose_name_plural = '员工管理'


class Order(models.Model):  # 订单
    # order_id = models.IntegerField('订单id', primary_key=True, unique=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.FloatField('总金额', null=False, blank=False, default=0)  # 订单总金额
    order_creation_time = models.DateTimeField('订单创建时间', auto_now_add=True)
    payment_method = models.CharField('支付方式', max_length=32, null=False, blank=False, default="在线支付")  # 支付方式
    name = models.CharField('收货人', max_length=32, null=False, blank=False, default="")  # 收货人
    telephone = models.CharField('联系方式', max_length=32, null=False, blank=False, default="")  # 联系方式
    area = models.CharField('省市区街道', max_length=256, null=False, blank=False, default="")  # 地址
    address = models.CharField('详细地址', max_length=256, null=False, blank=False, default="")  # 详细地址
    address_tag = models.CharField('地址标签', max_length=256, null=False, blank=False, default="")  # 地址标签
    real_payment = models.FloatField('实付款', null=False, blank=False, default=0)  # 实付款
    shipping = models.FloatField('运费', null=False, blank=False, default=0)  # 运费
    discounted_price = models.FloatField('优惠金额', null=False, blank=False, default=0)  # 优惠金额
    deposit = models.FloatField('定金', null=False, blank=False, default=0)  # 定金
    payment_status = models.BooleanField('支付状态', null=False, blank=False, default=False)
    def __str__(self):
        return str(self.id)

    class Meta:
        # 定义后台表显示名称
        verbose_name = '订单管理'
        verbose_name_plural = '订单管理'
    # def save(self):
    #     details = Order_detail.objects.filter(order=self)
    #     for detail in details:
    #         Commodity.objects.get(id=detail.commodity_id)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        # self.customer.consumption_amount += self.total_amount
        # self.customer.save()


class Order_detail(models.Model):  # 订单详情
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    # commodity_id = models.IntegerField('商品ID', null=False, blank=False, default=0)
    unit_price = models.FloatField('商品单价', null=True, blank=True, default=0)  # 商品单价
    quantity = models.IntegerField('商品数量', null=False, blank=False, default=0)  # 商品数量

    class Meta:
        # 定义后台表显示名称
        verbose_name = '订单明细'
        verbose_name_plural = '订单明细'

    def save(self, *args, **kwargs):
        self.unit_price = self.commodity.selling_price
        super(Order_detail, self).save(*args, **kwargs)
        self.order.total_amount += self.unit_price*self.quantity
        self.order.real_payment += self.unit_price*self.quantity
        self.order.save()


class Shipping_address(models.Model):  # 收货地址
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField('收货人', max_length=32, null=False, blank=False, default="")  # 收货人
    telephone = models.CharField('联系方式', max_length=32, null=False, blank=False, default="")  # 联系方式
    area = models.CharField('省市区街道', max_length=256, null=False, blank=False, default="")  # 地址
    address = models.CharField('详细地址', max_length=256, null=False, blank=False, default="")  # 详细地址
    address_tag = models.CharField('地址标签', max_length=256, null=False, blank=False, default="")  # 地址标签
    def __str__(self):
        return self.customer.user_name


class Shopping_cart_details(models.Model):  # 购物车详情
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    unit_price = models.FloatField('商品单价', null=False, blank=False, default=0)  # 商品单价
    quantity = models.IntegerField('商品数量', null=False, blank=False, default=0)  # 商品数量
    def __str__(self):
        return self.customer.user_name


class Sales(models.Model):  # 销售额
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField('日期')
    sales_amount = models.IntegerField('销售额', null=False, blank=False, default=0)
    def __str__(self):
        return str(self.staff.staff_name) + "  " + str(self.date)




