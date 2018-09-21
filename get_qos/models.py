from django.db import models
from users.models import User
import django.utils.timezone as timezone
from tinymce.models import HTMLField
import tinymce
from django.urls import reverse

# Create your models here.
class QoS_data(models.Model):
    ws_url=models.CharField(max_length=200,default='www.baidu.com',verbose_name='服务地址')#需进行采集数据的web服务的地址
    user= models.ManyToManyField(User) #一对一
    user_ip=models.CharField(max_length=20,default='0.0.0.0')#用户IP
    http_code=models.CharField(max_length=20,null=True,blank=True,verbose_name='HTTP状态码')#返回的HTTP状态码   数据库中允许为空，后台管理添加数据时允许为空
    namelookup_time=models.FloatField(null=True,blank=True,verbose_name='HTTP状态码')     #DNS解析所消耗的时间
    connect_time=models.FloatField(null=True,blank=True,verbose_name='DNS解析时间')        #建立连接所消耗的时间
    pretransfer_time=models.FloatField(null=True,blank=True,verbose_name='建立连接到准备传输所需时间')     #从建立连接到准备传输所消耗的时间
    starttransfer_time=models.FloatField(null=True,blank=True,verbose_name='建立连接到传输开始所需时间')  #从建立连接到传输开始消耗的时间
    redirect_time=models.FloatField(null=True,blank=True,verbose_name='重定向所消耗的时间')   # 重定向所消耗的时间
    total_time=models.FloatField(null=True,blank=True,verbose_name='总时间')      #传输结束所消耗的总时间
    header_size=models.IntegerField(null=True,blank=True,verbose_name='HTTP头部大小')   #HTTP头部大小
    size_download=models.IntegerField(null=True,blank=True,verbose_name='下载数据包大小') #下载数据包大小
    size_upload=models.IntegerField(null=True,blank=True,verbose_name='上传数据包大小')   #上传数据包大小
    speed_download=models.IntegerField(null=True,blank=True,verbose_name='平均下载速度')#平均下载速度
    speed_upload=models.IntegerField(null=True,blank=True,verbose_name='平均上传速度')  #平均上传速度
    add_time = models.DateTimeField(blank=True,default=timezone.now)
    price=models.FloatField(null=True,blank=True,verbose_name='价格')      #价格

class QoS_attributes(models.Model):
    meaning=models.CharField(max_length=200, null=False, blank=True)  # 属性名
    number=models.IntegerField(null=False,blank=False)  #属性编号
    is_collect=models.BooleanField(blank=False)#选择是否进行清洗

class Monitor(models.Model):
    user = models.ManyToManyField(User)  # 一对一
    ws_url=models.CharField(max_length=200,default='www.baidu.com')#需进行监控的web服务的地址
    is_monitor=models.BooleanField(default=0,blank=False)#选择是否进行监控
    tag=models.CharField(max_length=200,default='天气1')#需进行监控的web服务的地址

class Monitor_setting(models.Model):
    time_interval=models.IntegerField(null=False,blank=True,default=30)
    total_time=models.IntegerField(null=False,blank=True,default=7)
    user = models.ManyToManyField(User)  # 一对一


class Example_base(models.Model):
    type = models.CharField(max_length=50, null=False, blank=True)  # WEB服务类型
    bandwidth = models.FloatField(max_length=50, null=False, blank=True)
    workload = models.FloatField(max_length=50, null=False, blank=True)
    qos_time = models.FloatField(null=True,blank=True)


class Notice(models.Model):
    user = models.ManyToManyField(User)  # 一对一
    add_time = models.DateTimeField(blank=True,default=timezone.now)
    title = models.CharField(max_length=64)
    content = tinymce.models.HTMLField(verbose_name='文章详情')
    def get_absolute_url(self):
        return reverse('get_qos:article', kwargs={'id': self.id})

class QoS_datacaiji(models.Model):
    ws_url=models.CharField(max_length=200,default='www.baidu.com',verbose_name='服务地址')#需进行采集数据的web服务的地址
    user= models.ManyToManyField(User) #一对一
    user_ip=models.CharField(max_length=20,default='0.0.0.0')#用户IP
    http_code=models.CharField(max_length=20,null=True,blank=True,verbose_name='HTTP状态码')#返回的HTTP状态码   数据库中允许为空，后台管理添加数据时允许为空
    namelookup_time=models.FloatField(null=True,blank=True,verbose_name='HTTP状态码')     #DNS解析所消耗的时间
    connect_time=models.FloatField(null=True,blank=True,verbose_name='DNS解析时间')        #建立连接所消耗的时间
    pretransfer_time=models.FloatField(null=True,blank=True,verbose_name='建立连接到准备传输所需时间')     #从建立连接到准备传输所消耗的时间
    starttransfer_time=models.FloatField(null=True,blank=True,verbose_name='建立连接到传输开始所需时间')  #从建立连接到传输开始消耗的时间
    redirect_time=models.FloatField(null=True,blank=True,verbose_name='重定向所消耗的时间')   # 重定向所消耗的时间
    total_time=models.FloatField(null=True,blank=True,verbose_name='总时间')      #传输结束所消耗的总时间
    header_size=models.IntegerField(null=True,blank=True,verbose_name='HTTP头部大小')   #HTTP头部大小
    size_download=models.IntegerField(null=True,blank=True,verbose_name='下载数据包大小') #下载数据包大小
    size_upload=models.IntegerField(null=True,blank=True,verbose_name='上传数据包大小')   #上传数据包大小
    speed_download=models.IntegerField(null=True,blank=True,verbose_name='平均下载速度')#平均下载速度
    speed_upload=models.IntegerField(null=True,blank=True,verbose_name='平均上传速度')  #平均上传速度
    add_time = models.DateTimeField(blank=True,default=timezone.now)
    price=models.FloatField(null=True,blank=True,verbose_name='价格')      #价格




