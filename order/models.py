from django.db import models

from goods.models import Goods, Sku
from user.models import User

# Create your models here.
# 订单表


class Order(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 订单流水号
    sn = models.CharField(verbose_name='订单流水号', max_length=64, unique=True)
    # 用户
    id_user = models.ForeignKey(to=User, verbose_name='用户', related_name="orderitem_user", on_delete=models.SET_NULL, null=True)
    # 订单总数量
    total_count = models.IntegerField(verbose_name='订单总数量')
    # 订单总金额
    total_amount = models.DecimalField(verbose_name='订单总金额', max_digits=10, decimal_places=2)
    # 邮费
    postage = models.DecimalField(verbose_name='邮费', max_digits=4, decimal_places=2)
    # 用户订单备注
    user_remark = models.TextField(verbose_name='用户订单备注', null=True, blank=True)
    # 商家订单备注
    admin_remark = models.TextField(verbose_name='商家订单备注', null=True, blank=True)
    # 订单状态
    order_status_choices = (
        (1, '待支付'), (2, '已付款'), (3, '待收货'), (4, '已收获'), (5, '退款申请中'), (6, '待退货'), (7, '待退款'), (8, '已退货'), (9, '已退款'),
        (10, '已完成'), (-1, '异常')
    )
    order_status = models.IntegerField(verbose_name='订单状态', choices=order_status_choices, null=False, default=1)

    # 会员信息
    # 收货人
    consignee_user = models.ForeignKey(to=User, verbose_name='收货人', related_name="order_user", on_delete=models.SET_NULL, null=True, blank=True)
    # 收货人姓名
    consignee_name = models.CharField(verbose_name='收货人姓名', max_length=10, null=True, blank=True)
    # 收货人手机号
    consignee_phone = models.CharField(verbose_name='收货人手机号', max_length=11, null=True, blank=True)
    # 收货人地址
    consignee_address = models.TextField(verbose_name='收货人地址', null=True, blank=True, )

    # 支付信息
    # 实际支付总金额
    pay_amount = models.DecimalField(verbose_name='实际支付总金额', max_digits=10, decimal_places=2, null=True, blank=True)
    # 支付成功时间
    pay_time = models.DateTimeField(verbose_name='支付成功时间', null=True, blank=True)
    # 支付流水号
    pay_code = models.CharField(verbose_name='支付流水号', max_length=32, null=True, blank=True)
    # 支付方式
    pay_type_choices = ((0, ''), (1, '支付宝支付'), (2, '微信支付'),)
    pay_type = models.IntegerField(verbose_name='支付方式', choices=pay_type_choices, blank=True, default=0, )

    # 优惠券+减免=总金额
    discount_amount = models.DecimalField(verbose_name='优惠总金额', max_digits=10, decimal_places=2, null=True, blank=True)

    # 物流信息
    # 物流公司名称
    shipping_name = models.CharField(verbose_name='物流公司名称', max_length=50, null=True, blank=True)
    # 物流单号
    shipping_code = models.CharField(verbose_name='物流单号', max_length=50, null=True, blank=True)
    # 物流发货时间
    shipping_send_time = models.DateTimeField(verbose_name='物流发货时间', null=True, blank=True)
    # 物流收货时间
    shipping_receive_time = models.DateTimeField(verbose_name='物流收货时间', null=True, blank=True)

    # 外键关联查询的时候返回的值
    class Meta:
        verbose_name = "订单管理"  # 模型名称
        verbose_name_plural = "订单管理"  # 模型复数名称

    # Python 2 中返回表的表述
    def __unicode__(self):
        return self.sn

    # Python 3 中返回表的表述
    def __str__(self):
        return self.sn


# 订单表商品项
class OrderItem(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 商品spu id
    id_goods = models.ForeignKey(to=Goods, verbose_name='商品(Spu)ID', related_name="orderitem_goods",
                                 on_delete=models.SET_NULL, null=True)
    # sku id
    id_sku = models.ForeignKey(to=Sku, verbose_name='商品(Sku)ID', related_name="orderitem_sku",
                               on_delete=models.SET_NULL, null=True)
    # 订单流水号sn
    id_order = models.CharField(verbose_name='订单流水号', max_length=64)
    # 商品名称
    name = models.CharField(verbose_name='商品名称', max_length=120)
    # 商品价格
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    # 商品数量
    count = models.IntegerField(verbose_name='商品数量')
    # 订单总金额
    total_amount = models.DecimalField(verbose_name='订单总金额', max_digits=10, decimal_places=2)
    # 实际支付总金额
    pay_amount = models.DecimalField(verbose_name='实际支付总金额', max_digits=10, decimal_places=2, blank=True)
    # 商品图片
    pic = models.CharField(verbose_name='商品图片', max_length=256, )

    # 外键关联查询的时候返回的值
    class Meta:
        verbose_name = "订单商品管理"  # 模型名称
        verbose_name_plural = "订单商品管理"  # 模型复数名称

    # Python 2 中返回表的表述
    def __unicode__(self):
        return self.name

    # Python 3 中返回表的表述
    def __str__(self):
        return self.name