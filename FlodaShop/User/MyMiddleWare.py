from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from User.models import User


class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 允许不验证直接访问的路由列表
        exclude_list = ['/user/login/', '/user/signup/', '/user/logout/', '/user/api/add/', 'api/batchadd/<int:num>/']
        snowID = request.COOKIES.get('snowID')
        if request.path in exclude_list:
            return
        else:
            try:
                user = User.objects.get(pk=snowID)
                return
            except Exception as e:
                print(e)
                return redirect('User:login')