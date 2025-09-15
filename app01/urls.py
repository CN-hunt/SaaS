from django.contrib import admin
from django.urls import path, include

from app01 import views

urlpatterns = [
    path('email/', views.send_welcome_email, ),
    # 注册
    path('register/', views.register),
    path('register/confirm_email/', views.confirm_email),


]