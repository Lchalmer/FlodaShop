"""FlodaShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from User import views

app_name = 'User'
urlpatterns = [
    # 注册
    path('signup/', views.SignupView.as_view(), name='signup'),
    # 登陆
    path('login/', views.LoginView.as_view(), name='login'),
    # 登出
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 添加用户
    path('api/add/', views.AddUserView.as_view(), name='add'),
    # 批量随机
    path('api/batchadd/<int:num>/', views.BatchAddView.as_view(), name='batchadd'),
    # 检索，修改，删除
    path('api/handle/<int:pk>/', views.HandleView.as_view(), name='handle'),
]
