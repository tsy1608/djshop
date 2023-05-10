from django.contrib import admin

# Register your models here.
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    #################################################
    # 列表展示列参数
    #################################################
    # 1、显示的列表信息
    list_display = ('username', 'nickname', 'password', 'salt',)
    # 2、查询过滤的字段
    list_filter = ('nickname', 'sex',)
    # 3、搜索的字段
    search_fields = ('nickname', 'sex',)
    # 4、可编辑的字段
    list_editable = ('nickname', 'password', 'salt',)