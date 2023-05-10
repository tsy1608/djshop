from django.contrib import admin

# Register your models here.
from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 1、显示的列表信息
    list_display = (
        'sn', 'order_status', 'consignee_user', 'consignee_name', 'pay_amount', 'pay_code', 'pay_type', 'shipping_name',
        'shipping_code', 'postage', 'total_amount',)

    # 禁用后台添加功能
    def has_add_permission(self, request):
        return False

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # 1、显示的列表信息
    list_display = (
        'id_goods', 'id_sku', 'id_order', 'name', 'price', 'count', 'total_amount', 'pay_amount',)

    # 禁用后台添加功能
    def has_add_permission(self, request):
        return False