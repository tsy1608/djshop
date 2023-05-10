from django.db import models
from goods.models import Goods, Sku
from user.models import User

# Create your models here.
# 购物车表

class Cart(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 用户id，连接用户表
    id_user = models.ForeignKey(to=User, verbose_name='用户', related_name="cart_user", on_delete=models.SET_NULL,
                                null=True)
    # 商品id，连接商品表
    id_goods = models.ForeignKey(to=Goods, verbose_name='商品(Spu)', related_name="cart_goods", on_delete=models.SET_NULL,
                                 null=True)
    # skuid，连接sku表
    id_sku = models.ForeignKey(to=Sku, verbose_name='商品(Sku)', related_name="cart_sku", on_delete=models.SET_NULL,
                               null=True)
    # 购物车商品数量
    count = models.IntegerField(verbose_name='数量', )

    # 外键关联查询的时候返回的值
    class Meta:
        verbose_name = "购物车列表"  # 模型名称
        verbose_name_plural = "购物车列表"  # 模型复数名称
        unique_together = (("id_user", "id_goods", "id_sku"),)  # 复合组件

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.id_user, self.id_goods, self.id_sku)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.id_goods) + '-' + str(self.id_sku)