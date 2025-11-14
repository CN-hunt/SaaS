import json
import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from web import models
from django_redis import get_redis_connection
import uuid


def index(request):
    return render(request, 'index.html')


def prices(request):
    """套餐充值界面"""
    # 获取套餐
    policy_list = models.PricePolicy.objects.filter(category=2)
    return render(request, 'prices.html', {'policy_list': policy_list})


def payment(request, policy_id):
    """支付界面"""
    # 1. 价格策略（套餐）policy_id
    policy_object = models.PricePolicy.objects.filter(id=policy_id, category=2).first()
    if not policy_object:
        return redirect('price')

    # 2. 要购买的数量
    number = request.GET.get('number', '')
    if not number or not number.isdecimal():
        return redirect('price')
    number = int(number)
    if number < 1:
        return redirect('price')

    # 3. 计算原价
    origin_price = number * policy_object.price

    # 4.之前购买过套餐(之前掏钱买过）
    balance = 0
    _object = None
    if request.tracer.price_policy.category == 2:
        # 找到之前订单：总支付费用 、 开始~结束时间、剩余天数 = 抵扣的钱
        # 之前的实际支付价格
        _object = models.Transaction.objects.filter(user=request.tracer.user, status=2).order_by('-id').first()
        total_timedelta = _object.end_datetime - _object.start_datetime
        balance_timedelta = _object.end_datetime - datetime.datetime.now()

        if total_timedelta.days == balance_timedelta.days:
            # 按照价值进行计算抵扣金额
            balance = _object.price_policy / total_timedelta.days * (balance_timedelta.days - 1)
        else:
            balance = _object.price_policy / total_timedelta.days * balance_timedelta.days

    if balance >= origin_price:
        return redirect('price')

    context = {
        'policy_id': policy_object.id,
        'number': number,
        'origin_price': origin_price,
        'balance': round(balance, 2),
        'total_price': origin_price - round(balance, 2),
        # 'policy_object': policy_object,
        # 'transaction': _object
    }

    # 保存在Redis中
    conn = get_redis_connection()
    key = 'payment_{}'.format(request.tracer.user.email)
    conn.set(key, json.dumps(context), ex=60 * 30)

    # 这两个不可以放在context里面不然保存到Redis里面时会报错TypeError
    context['policy_object'] = policy_object
    context['transaction'] = _object

    return render(request, 'payment.html', context)


def pay(request):
    """订单生成以及支付宝跳转"""
    conn = get_redis_connection()
    key = 'payment_{}'.format(request.tracer.user.email)
    context_string = conn.get(key)
    if not context_string:
        return redirect('price')
    context = json.loads(context_string.decode('utf-8'))

    # 1. 数据库中生成交易记录（待支付）
    #   等支付成功之后，我们需要把订单的状态更新为已支付、开始&结束时间
    order_id = uuid.uuid4().hex[:6] + request.tracer.user.email
    total_price = context['total_price']
    models.Transaction.objects.create(
        status=1,
        order=order_id,
        user=request.tracer.user,
        price_policy_id=context['policy_id'],
        count=context['number'],
        price=total_price
    )

    # 构造字典
    params = {
        'app_id': "9021000157660876",
        'method': 'alipay.trade.page.pay',
        'format': 'JSON',
        'return_url': "http://127.0.0.1:8000/pay/notify/",  # 回调链接post
        'notify_url': "http://127.0.0.1:8000/pay/notify/",  # 回调链接get
        'charset': 'utf-8',
        'sign_type': 'RSA2',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'version': '1.0',
        'biz_content': json.dumps({
            'out_trade_no': order_id,
            'product_code': 'FAST_INSTANT_TRADE_PAY',
            'total_amount': total_price,
            'subject': "BugFlow payment"
        }, separators=(',', ':'))
    }

    # 获取待签名的字符串
    unsigned_string = "&".join(["{0}={1}".format(k, params[k]) for k in sorted(params)])
    print(unsigned_string)

    # 签名 SHA256WithRSA(对应sign_type为RSA2)
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
    from base64 import decodebytes, encodebytes

    # SHA256WithRSA + 应用私钥 对待签名的字符串 进行签名
    private_key = RSA.importKey(open("files/应用私钥RSA2048-敏感数据，请妥善保管.txt").read())
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(SHA256.new(unsigned_string.encode('utf-8')))

    # 对签名之后的执行进行base64 编码，转换为字符串
    sign_string = encodebytes(signature).decode("utf8").replace('\n', '')

    # 把生成的签名赋值给sign参数，拼接到请求参数中。

    from urllib.parse import quote_plus
    result = "&".join(["{0}={1}".format(k, quote_plus(params[k])) for k in sorted(params)])
    result = result + "&sign=" + quote_plus(sign_string)

    # gateway = "https://openapi.alipaydev.com/gateway.do" # 旧网关
    gateway = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
    pay_url = "{}?{}".format(gateway, result)

    return redirect(pay_url)


def pay_notify(request):
    """支付成功后触发的url，支付宝回调函数"""
    print(request.method)
    if request.method == "GET":
        # 仅跳转
        # return redirect('#')
        return HttpResponse("success")
    else:
        # 订单状态更新
        pass
    return HttpResponse("成功")
