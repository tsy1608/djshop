from django.apps import AppConfig


class OrderConfig(AppConfig):
    # 自定义主键的类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 模块的名称
    name = 'order'
    # 模块展示的名称
    verbose_name = "订单管理"