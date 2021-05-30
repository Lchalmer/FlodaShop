from django.db import models


# 商品
class Goods(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=18, decimal_places=2,  default=0.00)  # 价格
    # price = models.IntegerField(default=0)  # 价格
    discount = models.FloatField(default=0)  # 折扣
    expiration = models.DateTimeField(auto_now=True)  # 过期时间
    sketch = models.CharField(max_length=255)  # 简述
    description = models.CharField(max_length=255)  # 详情
    stock = models.IntegerField(default=0)  # 库存
    sales_volume = models.IntegerField(default=0)  # 销量
    pri_img = models.CharField(max_length=255, blank=True)  # 主图地址
    sec_img = models.CharField(max_length=255, blank=True)  # 次图地址
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.IntegerField(default=0)
    color = models.IntegerField(default=2, choices=[(1, 'Black'),
                                                    (2, 'Red'),
                                                    (3, 'Blue'),
                                                    (4, 'Green'),
                                                    (5, 'Pink')])
    size = models.IntegerField(default=1, choices=[(1, 'S'),
                                                   (2, 'M'),
                                                   (3, 'L'),
                                                   (4, 'XL')])
    flowerbrand = models.ForeignKey('Brand', models.CASCADE, related_name='flowers')  # 品牌

    class Meta:
        db_table = 'goods'

    def __str__(self):
        return self.name


# 品牌
class Brand(models.Model):
    bname = models.CharField(max_length=255)

    class Meta:
        db_table = 'brand'

    def __str__(self):
        return self.bname


# 评论
class Review(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.IntegerField(default=0)
    rating = models.IntegerField(default=3, choices=[(1, 'bad'),
                                                     (2, 'unwillingly'),
                                                     (3, 'medium'),
                                                     (4, 'good'),
                                                     (5, 'perfect')])
    flower = models.ForeignKey('Goods', models.CASCADE, related_name='review')
    user = models.ForeignKey('User.User', models.CASCADE, related_name='reviews', default=1)

    class Meta:
        db_table = 'review'


# 购物车记录
# class CartRecord(models.Model):
#     create_time = models.DateTimeField(auto_now_add=True)
#     num = models.IntegerField(default=1)  # 商品数量
#     flower = models.ForeignKey('Goods', models.CASCADE, related_name='cart')
#     buyer = models.ForeignKey('User.User', models.CASCADE, related_name='record', default=0)
#
#     class Meta:
#         db_table = 'cart'


# 订单
class Order(models.Model):
    order_id = models.IntegerField()  # 订单id
    goods_num = models.IntegerField(default=1)  # 商品数量
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0)  # 价格合计
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1, choices=[(1, '未支付'), (2, '未送达'), (3, '未评价'), ])
    user = models.ForeignKey('User.User', models.DO_NOTHING, related_name='order')

    class Meta:
        db_table = 'order'
