from django.contrib import admin
from django.urls import path, include
from web.views import account

from app01 import views

urlpatterns = [
    path('register/', account.register, name='register'),
    path('register/email/', account.confirm_email, name='confirm_email'),
]
