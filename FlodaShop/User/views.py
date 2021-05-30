import random
import time
from datetime import datetime, timedelta

from django.core import cache
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from User.UserSerializer import UserSignupSerializer, UserLoginSerializer
from User.models import User
from snowflake import maker_one


# 新增用户
class AddUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request):
        snowID = maker_one.CreateSnowID()
        user = self.serializer_class(data=request.data)
        if user.is_valid(raise_exception=True):
            user = User(snowID=snowID,
                        username=request.data['username'],
                        password=request.data['password'],
                        phone=request.data['phone'],
                        email=request.data['email'],
                        station=request.data['station'], )
            user.save()
        return render(request, 'login.html')


# 批量随机新增
class BatchAddView(APIView):
    def get(self, request, num):
        user_list = []
        for i in range(num):
            user = User(
                snowID=maker_one.CreateSnowID(),
                username=maker_one.CreateSnowID(),
                password='123',
                phone='18818712622',
                email='411928477@qq,com',
                station=1)
            user_list.append(user)
        User.objects.bulk_create(user_list)
        return Response({'msg': str(num) + '个对象创建成功!'})


# 检索，更新，删除用户
class HandleView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().using('slave01')
    # queryset = User.objects.all()
    serializer_class = UserSignupSerializer


# 注册
class SignupView(GenericAPIView):
    serializer_class = UserSignupSerializer

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        user = self.serializer_class(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
        return render(request, 'login.html')


# 登陆
class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user and user.password == password:
            # 缓存
            cache.cache.set('username', username, 60 * 60)  # 设置缓存
            # cookie
            response = redirect('Shop:home')
            expires = datetime.now() + timedelta(minutes=10)
            response.set_cookie('snowID', user.snowID, expires=expires)
            # 通过redis初始化购物车信息
            if not cache.cache.get(user.snowID):
                cart_list = []
                cache.cache.set(user.snowID, cart_list, 3600)
            return response
        else:
            return render(request, 'signup.html')


# 登出
class LogoutView(APIView):
    def get(self, request):
        response = redirect('User:login')
        response.delete_cookie('snowID')
        return response
