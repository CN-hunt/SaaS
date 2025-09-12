from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse
from django_redis import get_redis_connection  # 操作Redis


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '确认密码'}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '用户名'}),
            'email': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '邮箱'}),
            'password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '密码'}),
        }


class SendEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                                        "邮箱格式错误")])

    def clean_email(self):
        """邮箱存在校验钩子方法"""
        email = self.cleaned_data['email']

        # 校验数据库中是否已经存在邮箱
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")

        # 发邮件 & 写入 Redis

        # 邮件发送
        code = random.randrange(1000, 9999)  # 生成随机码
        subject = '邮箱验证码'  # 邮件标题
        from_email = settings.EMAIL_HOST_USER  # 发送方
        to = email  # 接收方
        text_content = '您好这是您的邮箱验证码:' + str(code)  # 邮件内容
        print(from_email)
        res = send_mail(subject, text_content, from_email, [to], )
        print(res)
        if res != 1:
            raise ValidationError("发送失败，请检查")

        conn = get_redis_connection()  # 获取Redis连接
        conn.set(email, code,ex=60)

        return email
