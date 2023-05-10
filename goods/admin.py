from django.contrib import admin
from django.utils.html import format_html

from goods.models import Image, Categorys, Goods, Sku


# Register your models here.
# 相册模块


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # 需要在后台展示的字段
    list_display = ('id', 'src_img', 'src',)
    # 编辑或者添加的时候展示的字段
    fields = ('src',)
    # 煤业显示条数
    list_per_page = 300
	# 自定义显示字段，用于显示预览图
    def src_img(self, obj):
        if obj.src and hasattr(obj.src, 'url'):
            return format_html('<img src="/%s" width="50px" />' % (obj.src,))
        else:
            return ''
	# 自定义显示字段对应的名称
    src_img.short_description = '相册图册'


# 注册商品分类模块
@admin.register(Categorys)
class CategorysAdmin(admin.ModelAdmin):
    # 需要在后台展示的字段
    list_display = ('name','src_img',  'src')
    # 编辑或者添加的时候展示的字段
    fields = ('name', 'src',)
	# 自定义显示字段，用于显示预览图
    def src_img(self, obj):
        if obj.src and hasattr(obj.src, 'url'):
            return format_html('<img src="/%s" width="50px" />' % (obj.src,))
        else:
            return ''
	# 自定义显示字段对应的名称
    src_img.short_description = '分类图片'


# 注册商品模块
@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    # 显示的列表信息
    list_display = ('name', 'price', 'descript', 'stock', 'like_num', 'id_category', 'pic_img', 'is_delete',)
    # 查询过滤的字段
    list_filter = ('is_hot', 'is_new', 'is_on_sale', 'is_delete',)
    # 搜索的字段
    search_fields = ('name',)
    # 可编辑的字段
    list_editable = ('price', 'stock',)
    # 分页，每页显示条数
    list_per_page = 10
    # 自定义字段，主图图片显示字段
    def pic_img(self, obj):
        return format_html('<img src="/%s" width="50px" />' % (obj.pic,))
	# 自定义显示字段对应的名称
    pic_img.short_description = '主图'
    pic_img.allow_tags = True


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    # 1、显示的列表信息
    list_display = ('id_goods', 'market_price', 'price', 'stock','attribute',)
    list_editable = ('market_price', 'price', 'stock',)