from django.contrib import admin

# Register your models here.
from cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    #################################################
    # 列表展示列参数
    #################################################
    # 1、显示的列表信息
    list_display = ('id_user', 'id_goods', 'id_sku', 'count', )
    # 2、可编辑的字段
    list_editable = ('count', )