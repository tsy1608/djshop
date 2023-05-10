# Generated by Django 3.2.4 on 2021-06-26 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0002_auto_20210627_0028'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('create_time', models.DateField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('modify_time', models.DateField(auto_now=True, null=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, null=True, verbose_name='是否删除')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('id_goods', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_goods', to='goods.goods', verbose_name='商品(Spu)')),
                ('id_sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_sku', to='goods.sku', verbose_name='商品(Sku)')),
                ('id_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_user', to='user.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车列表',
                'verbose_name_plural': '购物车列表',
                'unique_together': {('id_user', 'id_goods', 'id_sku')},
            },
        ),
    ]