from django.shortcuts import render, HttpResponse
from django.conf import settings
# 发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from django.http import JsonResponse


# 导入自己的用户模型

# Create your views here.


def send_welcome_email(request):
    subject = '邮箱验证码'  # 邮件标题
    from_email = settings.EMAIL_HOST_USER  # 发送方
    to = '2508734937@qq.com'  # 接收方
    text_content = '您好这是您的邮箱验证码'  # 邮件内容
    print(from_email)
    res = send_mail(subject, text_content, from_email, [to], )
    print(res)
    return HttpResponse('发送成功')


def register_views(request):
    return render(request, 'register.html')


@csrf_exempt
def confirm(request):
    if request.method == "POST":
        confirm_key = request.POST['confirm_key']
        print(confirm_key)
        return JsonResponse({'status': True})
