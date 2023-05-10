from django.apps import AppConfig


class GoodsConfig(AppConfig):
    # 自定义主键的类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 模块的名称
    name = 'goods'
    # 模块展示的名称
    verbose_name = "商品模块"
