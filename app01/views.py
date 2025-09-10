from django.shortcuts import render, HttpResponse
from django.conf import settings
# 发邮件
from django.core.mail import send_mail


# Create your views here.


def send_welcome_email(request):
    subject = 'Welcome to Plant'  # 邮件标题
    from_email = settings.EMAIL_HOST_USER  # 发送方
    to = '2508734937@qq.com'  # 接收方
    text_content = 'Welcome to Plant'  # 邮件内容
    print(from_email)
    res = send_mail(subject, text_content, from_email, [to],)
    print(res)
    return HttpResponse('发送成功')


