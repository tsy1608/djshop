from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.
# 用户表
class User(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 账号
    username = models.CharField(verbose_name='账号', max_length=30, unique=True, db_index=True)
    # 昵称
    nickname = models.CharField(verbose_name='昵称', max_length=30, null=True)
    # 密码
    password = models.CharField(verbose_name='密码', max_length=128, default='')
    # 加密盐
    salt = models.CharField(verbose_name='加密盐', max_length=30, default='', blank=True)
    # 个人简介
    introduce = models.TextField(verbose_name='个人简介',null=True, blank=True)
    # 头像
    avatar = models.ImageField(verbose_name='头像', upload_to='upload/avatar', null=True, blank=True)
    # 性别
    choices = (
        (1, '男'), (0, '女')
    )
    sex = models.IntegerField(verbose_name='性别', choices=choices, null=True)

    # 关联查询时返回的内容
    def natural_key(self):
        return {
            "id": str(self.id),
            "username": str(self.username),
            "nickname": str(self.nickname),
            "introduce": str(self.introduce),
            "avatar": str(self.avatar),
            "sex":str(self.sex)
        }

    # 外键关联查询的时候返回的值
    class Meta:
        verbose_name = "会员列表"  # 模型名称
        verbose_name_plural = "会员列表"  # 模型复数名称

    # 修改&添加提交时被执行，对密码进行加密
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 密码加密，使用盐值加密
        self.password = make_password(self.password, self.salt)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.username, self.nickname)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.username)