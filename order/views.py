from django.shortcuts import render
from userinfo.models import *
import datetime
# Create your views here.
a = [
    {"id":5,"title":"诺基亚7750蓝色","price":1000.00,"desc":"全面屏，2000万后置摄像头","amount":2,"trprice":1000.00},
    {"id":2,"title":"iphoneXs金色","price":8700.00,"desc":"全面屏，2000万后置摄像头","amount":3,"trprice":8700.00},
    {"id":3,"title":"iphoneXs玫瑰金","price":8700.00,"desc":"全面屏，2000万后置摄像头","amount":2,"trprice":8700.00},
    {"id":4,"title":"诺基亚7750黑色","price":1000.00,"desc":"全面屏，2000万后置摄像头","amount":1,"trprice":1000.00},
]

def addorder(request):
    if request.method == "POST":
        print(len(a))
        for m in a:
            print(m['id'])
        return render(request, 'login.html')
        # user = request.user
        # adsid = request.POST.get("adsid", "")
        # tomoney = request.POST.get("tomoney", "")
        # trmoney = request.POST.get("trmoney", "")
        # dealtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        glist = 
    elif request.method == "GET":
        return render(request,'login.html')
    # amount = models.IntegerField("数量", null=True, default=0)
    # bank = models.CharField("支付方式加卡号",max_length=50, null=False, default="unpay")
    # dealtime = models.DateTimeField("交易时间", auto_now_add=True)

    # title = models.CharField("商品名称", max_length=30, null=False, default="商品名称")
    # price = models.DecimalField('商品价格', max_digits=8, decimal_places=2)
    # desc = models.CharField('描述', max_length=1000, null=True)
    # amount = models.IntegerField("数量", null=True, default=0)
    # trprice = models.DecimalField('商品价格', max_digits=8, decimal_places=2)
    # order = models.ForeignKey(Order)

