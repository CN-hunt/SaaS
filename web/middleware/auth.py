from django.utils.deprecation import MiddlewareMixin
from web import models


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        如果中间件返回值了就说明用户无法访问，中间件返回什么，用户就稚只能看到什么
        如果用户已经登录则request中赋值
        """
        user_id = request.session.get('user_id',0)  # 如果用户登录了，那么这个数据肯定是有的
        user_object = models.UserInfo.objects.filter(id=user_id).first()  # 确认当前登录用户是不是你
        request.tracer = user_object
