from django.db import models

# Create your models here.
# 商品图片表
class Image(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 上传图片，上传到项目的upload文件夹中
    src = models.ImageField(verbose_name='商品图片', upload_to='upload')

    # 外键关联查询的时候返回的值
    def natural_key(self):
        # 获取图片地址的时候自动添加服务器地址
        return ('http://127.0.0.1:8000/' + str(self.src))

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.src,)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.src)

    # 定义当前model的参数
    class Meta:
        verbose_name = "商品相册"  # 模型名称
        verbose_name_plural = "商品相册"  # 模型复数名称



# 商品分类表
class Categorys(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 商品分类名称
    name = models.CharField(verbose_name='分类名称', max_length=20, null=False)
    # 商品分类图片
    src = models.ImageField(verbose_name='分类图片', upload_to='upload/categorys', null=True, blank=True)

    # 外键关联查询的时候返回的值
    def natural_key(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "src": str(self.src),
        }

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.name, self.src)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.name)

    # 定义当前model的参数
    class Meta:
        verbose_name = "商品分类"  # 模型名称
        verbose_name_plural = "商品分类"  # 模型复数名称


# 商品公共属性表spu
class Goods(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 商品描述
    descript = models.CharField(verbose_name='商品描述', max_length=255, blank=True)
    # 商品详情模板
    detail = models.TextField(verbose_name='商品详情模板', blank=True, )
    # 商品图片集合
    gallery = models.ManyToManyField(to=Image, verbose_name='商品图片集合', related_name="goods_gallery", )
    # 商品分类ID
    id_category = models.ForeignKey(to=Categorys, verbose_name='商品分类ID', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    # 商品图片
    pic = models.ForeignKey(to=Image, verbose_name='商品图片', on_delete=models.SET_NULL, null=True, blank=True)
    # 商品名称
    name = models.CharField(verbose_name='商品名称', max_length=128, unique=True, db_index=True)
    # 商品价格
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    # 商品库存
    stock = models.IntegerField(verbose_name='商品库存')
    # 是否热门
    is_hot = models.BooleanField(verbose_name='是否热门', default=False)
    # 是否新品
    is_new = models.BooleanField(verbose_name='是否新品', default=False)
    # 是否上架
    is_on_sale = models.BooleanField(verbose_name='是否上架', default=False)
    # 商品收藏量
    like_num = models.IntegerField(verbose_name='商品收藏量', null=True, blank=True)

    # 外键关联查询的时候返回的值
    def natural_key(self):
        return {
            "id": str(self.id),
            "descript": str(self.descript),
            "gallery": str(self.gallery),
            "id_category": str(self.id_category),
            "pic": str(self.pic),
            "name": str(self.name),
            "price": str(self.price),
            "stock": str(self.stock),
            "is_hot": str(self.is_hot),
            "is_new": str(self.is_new),
            "is_on_sale": str(self.is_on_sale),
            "like_num": str(self.like_num),
            # "detail": str(self.detail),
        }

    # 定义当前model的参数
    class Meta:
        ordering = ['id', 'name']  # 按照哪个字段排序
        verbose_name = "商品(Spu)"  # 模型名称
        verbose_name_plural = "商品(Spu)"  # 模型复数名称

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.name)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.id) + "-" + self.name


# 商品个体属性表sku
class Sku(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    id = models.AutoField(verbose_name='id', primary_key=True, unique=True)
    # 创建时间，增加时自动添加
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True, null=True)
    # 修改时间，修改时自动添加
    modify_time = models.DateField(verbose_name='修改时间', auto_now=True, null=True)
    # 是否删除
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, null=True)

    # 商品(Spu)
    id_goods = models.ForeignKey(to=Goods, verbose_name='商品(Spu)', on_delete=models.SET_NULL, null=True)
    # 商品属性键值对[属性名:属性值，多个属性使用"逗号"隔开]
    attribute = models.TextField(verbose_name='属性名:属性值，多个属性使用"逗号"隔开', null=True)
    # 市场价
    market_price = models.DecimalField(verbose_name='市场价', max_digits=10, decimal_places=2)
    # 真实价格
    price = models.DecimalField(verbose_name='真实价格', max_digits=10, decimal_places=2)
    # 商品库存
    stock = models.IntegerField(verbose_name='商品库存')

    # 修改sku库存的时候同步修改spu库存
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 查询所有的sku
        list_sku = Sku.objects.filter(id_goods_id=self.id_goods).all()
        total_stock = 0
        # 循环累加库存
        for s in list_sku:
            if s.id != self.id:
                total_stock = total_stock + s.stock
        total_stock = total_stock + self.stock
        # 查询对应的spu
        goods = Goods.objects.filter(id=self.id_goods_id).first()
        # 修改spu的库存
        goods.stock = total_stock
        # 保存修改
        goods.save()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    # 关联查询时返回的内容
    def natural_key(self):
        return {
            "id": str(self.id),
            "id_goods": str(self.id_goods),
            "attribute": str(self.attribute),
            "market_price": str(self.market_price),
            "price": str(self.price),
            "stock": str(self.stock),
        }

    # 定义当前model的参数
    class Meta:
        verbose_name = "商品(Sku)"  # 模型名称
        verbose_name_plural = "商品(Sku)"  # 模型复数名称

    # Python 2 中返回表的表述
    def __unicode__(self):
        return (self.attribute)

    # Python 3 中返回表的表述
    def __str__(self):
        return str(self.attribute)