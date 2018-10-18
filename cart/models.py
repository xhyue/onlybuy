from django.db import models
from userinfo.models import UserInfo
from memberapp.models import *
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey(GoodsDetail)
    amount = models.IntegerField("数量", null=True, default=0)

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey(Goods)

    def __str__(self):
        return self.user.username