from django.shortcuts import render, HttpResponse
from django.conf import settings
# 发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from django.http import JsonResponse

# 导入自己的用户模型,已经将所有的forms单独在一个文件里面
from web.forms.account import RegisterModelForm


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})


@csrf_exempt
def confirm_email(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        return JsonResponse({'status': True})
