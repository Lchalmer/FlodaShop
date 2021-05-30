# @Time: 2021-4-30  15:34
# @Author: chalmer
# @File: ShopSerializer.py
# @software: PyCharm
from rest_framework import serializers

from Shop.models import Goods, Brand, Review, Order


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        exclude = ['create_time', 'update_time', 'is_delete']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['bname']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['create_time', 'is_delete']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['create_time']
