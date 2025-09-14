from django.shortcuts import render, HttpResponse
from django.conf import settings
# 发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from django.http import JsonResponse

# 导入自己的用户模型,已经将所有的forms单独在一个文件里面
from web.forms.account import RegisterModelForm, SendEmailForm


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(request.POST)
    if form.is_valid():
        # 保存至数据库且密码需为密文，可以在模型文件的钩子方法中处理，直接在那里把返回的数据修改
        print(form.cleaned_data)  # 打印拿到的数据
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def send_email(request):
    """邮箱验证"""
    if request.method == "GET":
        print(request.GET.get("email"))
        # print(request.GET.get("tpl"))

        # tpl = request.GET.get("tpl")  # 用来确认前端返回的是register还是login
        # template_id = settings.TENCENT_EMAIL_TEMPLATE['tpl'] # register or login

        # 由于SendEmailForm里面只写了email这一个字段，所以这个form也只会校验前端返回的email数据
        form = SendEmailForm(data=request.GET)
        if form.is_valid():  # 这一步验证通过后其实就会执行完钩子方法中的所有内容，包括邮件发送
            # 发邮件并且写入Redis
            return JsonResponse({'status': True, })

        # form会帮助我们进行校验，所以就可以直接获取错误信息
        return JsonResponse({'status': False, 'error': form.errors})
