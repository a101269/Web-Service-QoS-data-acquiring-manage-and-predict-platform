
from django.db import models
from users.models import User
import django.utils.timezone as timezone
from django.urls import reverse
# Create your models here.
class Webservice(models.Model):
    user = models.ManyToManyField(User)  # 一对一
    number = models.IntegerField(null=False, blank=False)  #服务编号
    name=models.CharField(max_length=200)#服务名称
    type=models.CharField(max_length=200)#类别
    tag = models.CharField(max_length=50)  # 标签
    supplier=models.CharField(max_length=200)#服务提供商
    register_date=models.DateField(blank=True, default=timezone.now)
    feature=models.CharField(max_length=300)#特色
    description=models.CharField(max_length=1000)#服务描述

    ws_address=models.CharField(max_length=200)#web服务的地址
    request_method=models.CharField(max_length=50)#服务请求方式
    example=models.CharField(max_length=200)#请求示例
    price=models.FloatField()#价格
    input_parameter=models.CharField(max_length=50)#接口参数
    return_parameter=models.CharField(max_length=50)#返回参数
    result_type=models.CharField(max_length=20)#返回数据类型

class Collection_list(models.Model):
    user = models.ManyToManyField(User)  # 一对一
    number = models.IntegerField(null=False, blank=False)  # 服务编号



class Arma_resu(models.Model):
    url=models.CharField(max_length=200)#web服务的地址
    total_time = models.FloatField(null=False, blank=False)  # 服务编号