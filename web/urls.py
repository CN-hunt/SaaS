from django.contrib import admin
from django.urls import path, include
from web.views import account

from app01 import views

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send/email/', account.send_email, name='send_email'),
]
