from django.apps import AppConfig


class CartConfig(AppConfig):
    # 自定义主键的类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 模块的名称
    name = 'cart'
    # 模块展示的名称
    verbose_name = "购物车模块"
