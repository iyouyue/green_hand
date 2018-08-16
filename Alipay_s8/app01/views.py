from django.shortcuts import render, redirect, HttpResponse
import json
import time
from utils.pay import AliPay
from app01 import models
from django.conf import settings

def alipay_obj():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url="http://47.93.4.198:8004/page2/",
        return_url="http://47.93.4.198:8004/page3/",
        app_private_key_path="keys/app_private_2048.txt",
        alipay_public_key_path="keys/alipay_public_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay

def page1(request):
    if request.method == "GET":
        return render(request, 'page1.html')
    else:
        # 根据：appid、应用私钥、支付宝公钥、金额、订单名称、订单号 生一个URL，再进行跳转。
        # 1. 要支付的金额
        money = float(request.POST.get('money'))

        alipay = alipay_obj()

        order_num = "xxxxxxxxxxxx" + str(time.time())

        # 生成支付的url
        query_params = alipay.direct_pay(
            subject="充气式文杰",  # 商品简单描述
            out_trade_no=order_num,  # 商户订单号：ijldsddfsdfsdf
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )

        # 3. query_params，根据appid、应用私钥、支付宝公钥、金额、订单名称、订单号生成的参数。

        # 4. 拼接URL： https://openapi.alipaydev.com/gateway.do + query_params
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)


        # ####### 在数据库中生成订单 ###########
        models.Order.objects.create(num=order_num,price=money)

        return redirect(pay_url)


def page2(request):
    """
    支付宝支付成功后，支付宝主动向我的网站发送：post请求，用于通知我支付成功，我来修改订单状态
    PS: 检验数据是否合法
    :param request:
    :return:
    """
    alipay = alipay_obj()

    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        # 使用sign+支付宝发来的数据，进行校验
        status = alipay.verify(post_dict, sign)
        if status:
            order_num = post_dict.get('out_trade_no')
            models.Order.objects.filter(num=order_num).update(status=2)

        return HttpResponse('POST返回')


def page3(request):
    alipay = alipay_obj()
    params = request.GET.dict()
    sign = params.pop('sign', None)
    status = alipay.verify(params, sign)
    if status:
        return HttpResponse('支付成功')
    else:
        return HttpResponse('支付失败')


def page4(request):
    order_list = models.Order.objects.all()
    return render(request,'order_list.html',{'order_list':order_list})