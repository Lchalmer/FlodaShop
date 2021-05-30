from django.core import cache
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

# 首页
from Shop.ShopSerializer import GoodsSerializer, ReviewSerializer, BrandSerializer
from Shop.homepagination import HomePagination
from Shop.models import Goods, Review

# class HomeView(APIView):
#     def get(self, request):
#         return render(request, 'index.html')
from User.models import User


class HomeView(GenericAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self, request):
        # 新上架产品
        # 按创建时间从数据库中查询最新创建的数据，切片取前十二条
        new_goods = self.get_queryset().order_by('-create_time')[:12]
        new_listing = GoodsSerializer(instance=new_goods, many=True).data

        # 畅销产品
        # 取数据库中销量最高的数据，切片取前6条
        active_goods = self.get_queryset().order_by('-sales_volume')[:6]
        active_listing = GoodsSerializer(instance=active_goods, many=True).data

        # 获取登陆用户信息
        snowID = request.COOKIES.get('snowID')
        user = User.objects.get(pk=snowID)

        # 处理购物车信息
        cart_list = cache.cache.get(snowID)
        cart_goods_num = len(cart_list)
        clist = []
        total = 0
        for gid in cart_list:
            goods = Goods.objects.get(pk=gid)
            total += float(goods.price) * float(1 - goods.discount)
            clist.append(goods)
        final_total = total * 1.22
        return render(request, 'index.html', context=locals())


# 店铺
class ShopView(GenericAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = HomePagination

    def get(self, request):
        snowID = request.COOKIES.get('snowID')
        user = User.objects.get(pk=snowID)
        goods = self.get_queryset().filter(is_delete=0)
        goods_dict = GoodsSerializer(instance=goods, many=True).data
        # 处理购物车信息
        cart_list = cache.cache.get(snowID)
        cart_goods_num = len(cart_list)
        clist = []
        total = 0
        for gid in cart_list:
            goods = Goods.objects.get(pk=gid)
            total += float(goods.price) * float(1 - goods.discount)
            clist.append(goods)
        final_total = total * 1.22
        return render(request, 'shop.html', locals())


# 商品详情
class DetailView(APIView):
    def get(self, request, gid):
        goods = GoodsSerializer(instance=Goods.objects.get(pk=gid)).data
        reviews_count = len(Review.objects.filter(flower=goods['id']))
        snowID = request.COOKIES.get('snowID')
        user = User.objects.get(pk=snowID)
        # 处理购物车信息
        cart_list = cache.cache.get(snowID)
        cart_goods_num = len(cart_list)
        clist = []
        total = 0
        for gid in cart_list:
            flower = Goods.objects.get(pk=gid)
            total += float(flower.price) * float(1 - flower.discount)
            clist.append(flower)
        final_total = total * 1.22
        return render(request, 'product-details.html', locals())


# 添加商品
class AddGoodsView(CreateAPIView):
    serializer_class = GoodsSerializer


# 添加品牌
class AddBrandView(CreateAPIView):
    serializer_class = BrandSerializer


# 添加评论
class AddReviewView(CreateAPIView):
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            id = data['flower'].value
        return redirect('/index/detail/{}/'.format(id))


# 商品检索，更新，删除操作
class HandleGoodsView(RetrieveUpdateDestroyAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


# 购物车处理
class AddCartView(CreateAPIView):
    def get(self, request, gid):
        snowID = request.COOKIES.get('snowID')
        user = User.objects.get(pk=snowID)
        cart_list = cache.cache.get(snowID)
        cart_list.append(gid)
        cache.cache.set(snowID, cart_list, 3600)
        return redirect('/index/detail/{}/'.format(gid))


# 从购物车删除
class DelCartView(CreateAPIView):
    def get(self, request, gid):
        snowID = request.COOKIES.get('snowID')
        user = User.objects.get(pk=snowID)
        cart_list = cache.cache.get(snowID)
        cart_list.remove(gid)
        cache.cache.set(snowID, cart_list, 3600)
        return redirect('/index/detail/{}/'.format(gid))
