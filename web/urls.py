from django.contrib import admin
from django.urls import path, include
from web.views import account,home

from app01 import views

urlpatterns = [
    # 注册
    path('register/', account.register, name='register'),
    path('send/email/', account.send_email, name='send_email'),

    # 登录
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),
    path('logout',account.logout,name='logout'),

    # 主页
    path('index/',home.index,name='index'),
]
