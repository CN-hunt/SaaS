from django import forms
from django.shortcuts import render, HttpResponse
from django.conf import settings
# 发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from django.http import JsonResponse

# 导入自己的用户模型
from app01 import models

# redis
import redis


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '确认密码'}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '用户名'}),
            'email': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '邮箱', 'id': 'EM'}),
            'password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '密码'}),
        }


def send_welcome_email(request):
    subject = '邮箱验证码'  # 邮件标题
    from_email = settings.EMAIL_HOST_USER  # 发送方
    to = '2508734937@qq.com'  # 接收方
    text_content = '您好这是您的邮箱验证码'  # 邮件内容
    print(from_email)
    res = send_mail(subject, text_content, from_email, [to], )
    print(res)
    return HttpResponse('发送成功')


@csrf_exempt
def confirm_email(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        return JsonResponse({'status': True})


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
