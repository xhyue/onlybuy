from django.shortcuts import render
from django.http import request, response, HttpResponse
from userinfo.models import *
from .models import *
import datetime
from django.db import DatabaseError
from userinfo.views import check_login_status
import logging
from django.core import serializers
import json
from cart.models import *
import decimal
from pay import views as payview
from django.db.models import Q
# Create your views here.
# goods = [
#     {"id":5,"title":"诺基亚7750蓝色","price":1000.00,"desc":"全面屏，2000万后置摄像头","amount":2,"trprice":1000.00},
#     {"id":2,"title":"iphoneXs金色","price":8700.00,"desc":"全面屏，2000万后置摄像头","amount":3,"trprice":8700.00},
#     {"id":3,"title":"iphoneXs玫瑰金","price":8700.00,"desc":"全面屏，2000万后置摄像头","amount":2,"trprice":8700.00},
#     {"id":4,"title":"诺基亚7750黑色","price":1000.00,"desc":"全面屏，2000万后置摄像头","amount":1,"trprice":1000.00},
# ]


# {"adsid":,"tprice":,"trmoney":,"tamount":,"bank":,goods":[{"id":,"amount":,"price":}]}
# 订单
@check_login_status
def add_order(request):
    if request.method == "POST":
        user = request.user
        adsid = request.POST.get("adsid", "")
        tomoney = decimal.Decimal(request.POST.get("tprice", ""))
        trmoney = decimal.Decimal(request.POST.get("trmoney", ""))
        goods = json.loads(request.POST.get("goods", ""))
        dealtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        orderNo =dealtime
        mtomoney = 0
        ftomoney = 0
        amount = 0
        postprice = 10
        ads = Address.objects.filter(id=adsid)[0]
        glist = list()
        lam_order = Order()
        if tomoney > 99:
            postprice = 0
        gstr = ''
        # 计算总金额是否一致,总数量
        for good in goods:
            cartid = good["id"]
            cart_goods = Cart.objects.filter(id=cartid)
            goods_price = cart_goods[0].goods.price
            fgoods_price = decimal.Decimal(good["price"])
            fgoods_amount = good["amount"]
            amount = amount + int(fgoods_amount)
            mtomoney = mtomoney+goods_price*int(fgoods_amount)
        if mtomoney == tomoney and postprice+mtomoney == trmoney:
            order = Order.objects.create(orderNo=orderNo, ads=ads, tomoney=tomoney, trmoney=trmoney, amount=amount,dealtime=dealtime, status=0, user=user)
            for good in goods:
                cartid = good["id"]
                cart_goods = Cart.objects.filter(id=cartid)
                goods_img = cart_goods[0].goods.listimg
                goods_color = cart_goods[0].color
                goods_spec = cart_goods[0].spec
                goods_price = cart_goods[0].goods.price
                fgoods_price = decimal.Decimal(good["price"])
                fgoods_amount = good["amount"]
                glist.append(
                    OrderGoods(title=cart_goods[0].goods.title, price=goods_price, desc=cart_goods[0].goods.desc,
                               amount=fgoods_amount, goodsimg=goods_img, color=goods_color, spec=goods_spec, trprice=fgoods_price,
                               order=order))
                if gstr != '':
                    gstr = gstr + ',' + str(good['id'])
                else:
                    gstr = str(good['id'])
            OrderGoods.objects.bulk_create(glist)
            try:
                Cart.objects.extra(where=['id IN (' + gstr + ')']).delete()
            except DatabaseError as e:
                logging.warning(e)
        else:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "金额错误"}))
        return HttpResponse(json.dumps({"result": True, "data":order.orderNo, "error": ""}))


def tomoney(request):
    if request.method == 'GET':
        orderno = request.GET.get("orderno")
        order = Order.objects.filter(orderNo=orderno)
        trmoney = str(order[0].trmoney)
        banklist = payview.banklist()
        return HttpResponse(json.dumps({"result": True, "data":{"banklist":banklist,"trmoney":trmoney}, "error": ""}))


@check_login_status
def order_goods(request):
    if request.method == 'GET':
        user = request.user
        cartids = request.GET.getlist("cartids")
        ordergoods = []
        for cartid in cartids:
            a = {}
            cart = Cart.objects.filter(id=cartid)[0]
            a["cartid"] = cart.id
            a["title"] = cart.goods.title
            a["desc"] = cart.goods.desc
            a["img"] = "/images" + str(cart.goods.listimg)
            a["color"] = cart.color
            a["spec"] = cart.spec
            a["price"] = str(cart.price)
            ordergoods.append(a)
        return HttpResponse(json.dumps({"result": True, "data": ordergoods, "error":""}))

# orderst:全部订单0，待付款1，待收货2，待评价3，已取消4
@check_login_status
def order_list(request):
    if request.method == "GET":
        user = request.user
        orderst=request.GET.get("orderst","0")
        print(orderst)
        if orderst == "0":
            orderlist = Order.objects.filter(user_id=user.id)
        elif orderst == "1":
            orderlist = Order.objects.filter(Q(user_id=user.id)&Q(status=0)|Q(status=4))
        elif orderst == "2":
            orderlist = Order.objects.filter(Q(user_id=user.id)&Q(status=1)|Q(status=2))
        elif orderst == "3":
            orderlist = Order.objects.filter(user_id=user.id, status=3)
        elif orderst == "4":
            orderlist = Order.objects.filter(Q(user_id=user.id)&Q(status=5)|Q(status=6))
        orderlists = []
        if len(orderlist)>0:
            for order in orderlist:
                orderlistt = {}
                orderlistt['orderNo'] = order.orderNo
                orderlistt['orderid'] = order.id
                orderlistt['status'] = order.status
                # orderlistt['ads'] = order.ads
                orderlistt['tomoney'] = str(order.tomoney)
                orderlistt['trmoney'] = str(order.trmoney)
                orderlistt['amount'] = order.amount
                orderlistt['bank'] = order.bank
                orderlistt['dealtime'] = order.dealtime.strftime("%Y-%m-%d %H:%M:%S")
                goods = order.ordergoods_set.all()
                goodss = serializers.serialize("json", goods)
                orderlistt['goodss'] = goodss
                orderlists.append(orderlistt)
            return HttpResponse(json.dumps({"result": True, "list": orderlists}))
        else:
            return HttpResponse(json.dumps({"result": False, "list": ""}))


def cancel_order(request):
    if request.method == "GET":
        user = request.user
        orderid = request.GET.get("orderid","")
        Order.objects.filter(id=orderid, user=user).update(status=5)
        return HttpResponse(json.dumps({"result": True, "msg": "订单已取消"}))


def order_detail(request):
    if request.method == "GET":
        user = request.user
        orderid = request.GET.get("orderid", "")
        orderdetail = Order.objects.filter(id=orderid, user=user)
        orderdetail = serializers.serialize("json", orderdetail)
        return HttpResponse(json.dumps({"result": True, "orderdetail": orderdetail}))


# 订单号 订单状态 联系人 邮编 电话 地址
def logistics_info(request):
    if request.method == "GET":
        user = request.user
        orderid = request.GET.get("orderid", "")
        order = Order.objects.filter(id=orderid)
        log = Logistics.objects.filter(order_id=orderid)
        pass







