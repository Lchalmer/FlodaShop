# @Time: 2021-4-29  22:24
# @Author: chalmer
# @File: UserSerializer.py
# @software: PyCharm
from rest_framework import serializers

from User.models import User


# 用户注册认证
class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'email', 'station']


# 用户登陆认证
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']