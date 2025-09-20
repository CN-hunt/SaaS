from django.contrib import admin
from django.urls import path, include
from web.views import account, home, project, manage

from app01 import views

urlpatterns = [
    # 注册
    path('register/', account.register, name='register'),
    path('send/email/', account.send_email, name='send_email'),

    # 登录
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),
    path('logout', account.logout, name='logout'),

    # 主页
    path('index/', home.index, name='index'),

    # 项目列表
    path('project/list/', project.project_list, name='project_list'),

    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    # 项目管理
    path('manage/<int:project_id>/', include([
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),
        path('file/', manage.file, name='file'),
        path('wiki/', manage.wiki, name='wiki'),
        path('setting/', manage.setting, name='setting'),
    ], )),

]
