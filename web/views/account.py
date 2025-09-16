from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
# 发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from django.http import JsonResponse
from web import models

# 导入自己的用户模型,已经将所有的forms单独在一个文件里面
from web.forms.account import RegisterModelForm, SendEmailForm, LoginForm

from django.db.models import Q  # 构造复杂查询


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'rgs.html', {'form': form})
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


def login(request):
    """用户名密码登录"""
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(password=password).first()  # 邮箱也可以实现登录
        if user_object:
            # 只有当用户名和密码存在正确时才允许跳转
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60*60*24*7)   # 用户登录成功后重写session数据为两周
            return redirect('/index/')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """图片验证码生成"""
    from utils.picture import generate_captcha
    from io import BytesIO

    img_object, code = generate_captcha()

    request.session['image_code'] = code  # 写入session
    request.session.set_expiry(60)  # 设置session的超时时间，不然默认是两周、

    stream = BytesIO()  # 图片写入内存
    img_object.save(stream, format='PNG')  # 图片写入内存

    stream.getvalue()  # 得到写入内存的图片
    print(code)
    return HttpResponse(stream.getvalue(), )  # 在得到内存中写入的数据后返回给前端


def logout(request):
    request.session.flush()  # 清空session数据
    return redirect('/index/')