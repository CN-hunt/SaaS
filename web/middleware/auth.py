from datetime import datetime

from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import redirect
from django.conf import settings
import datetime


class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        如果中间件返回值了就说明用户无法访问，中间件返回什么，用户就稚只能看到什么
        如果用户已经登录则request中赋值
        """
        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)  # 如果用户登录了，那么这个数据肯定是有的
        user_object = models.UserInfo.objects.filter(id=user_id).first()  # 确认当前登录用户是不是你

        request.tracer.user = user_object

        # 添加白名单，用户不登录也能看见的界面
        # request.path_info 可以查看当前用户访问的url
        # settings.WHITE_REGEX_URL_LIST   获取写在settings.py中的白名单
        print(request.path_info)
        if request.path_info in settings.WHITE_REGEX_URL_LIST:  # 如果用户访问的url在白名单中则放行
            return
        if not request.tracer.user:  # 否则判断其是否登录，未登录者返回登录界面
            return redirect('login')

        # 用户登录成功后，访问后台管理时获取用户当前的额度
        # 获取当前用户id最大值（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy_category=1).first()

        request.tracer.price_policy = _object.price_policy

    def process_view(self, request, view, args, kwargs):

        # 判断url是否以manage开头
        if not request.path_info.startswith('/manage/'):
            return

        project_id = kwargs.get('project_id')

        # 判断是否为本人创建
        project_object = models.Project.objects.filter(
            creator=request.tracer.user,
            id=project_id
        ).first()
        if project_object:
            # 本人创建则返回
            request.tracer.project = project_object
            return

        # 是否为本人参与项目
        project_user_object = models.ProjectUser.objects.filter(
            user=request.tracer.user, project_id=project_id
        ).first()
        if project_user_object:
            # 确认为本人参与
            request.tracer.project = project_user_object.project
            return

        return redirect('project_list')
