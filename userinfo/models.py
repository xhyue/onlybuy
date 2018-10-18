from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
SEX_CHOISE = (
    (0, "男"),
    (1, "女")
)
class UserInfo(AbstractUser):
    gender = models.IntegerField("性别", choices=SEX_CHOISE, default=0)
    mobile = models.CharField("手机号", max_length=13, null=False)
    email = models.EmailField("email", null=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    consignee = models.CharField("收件人", max_length=20, null=False, default="any")
    ads = models.TextField("收货地址",null=False)
    mobile = models.CharField("手机号", max_length=13, null=False)
    defaultads = models.BooleanField("是否为默认地址", default=False)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.user.username

