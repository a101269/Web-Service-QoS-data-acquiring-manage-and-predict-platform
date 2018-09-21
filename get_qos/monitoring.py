import os
import sys
sys.path.append('F:\\PycharmProjects\wbqossite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wbqossite.settings")# project_name 项目名称
import django
django.setup()
from get_qos.models import Example_base
from get_qos.models import QoS_data
from get_qos.models import Monitor
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from users.models import User
from get_qos.getqos_threads import qosthread
from threading import Thread


# print("hello")
# case = Example_base(type="计算", bandwidth=1000, workload=1000, qos_time=250)
# case.save()
# var = 1
# while var == 1:  # 表达式永远为 true
#     num = int(input("输入一个数字  :"))
#     print("你输入的数字是: ", num)
#
# print("Good bye!")
#
# threads = []
# i=0
# monitoring_list = Monitor.objects.filter(user=request.user,is_monitor=1)
# n=len(monitoring_list)
# records=[]
# listy=[]
# for ws in monitoring_list:     #创建线程列
#     t = qosthread(i,ws.ws_url,request.user.email,0)
#     i+=1
#     threads.append(t)
# for t in threads:#各个线程开始进行监测?
#     t.start()
#     print(t.threadID)
# for ws in monitoring_list:     #创建线程列表
#     records.append(QoS_data.objects.filter(user=request.user, ws_url=ws.ws_url).latest('add_time'))  # 各个web服务对应的最新QOS数据
# for m in range(n):
#     listy.append(records[m].total_time)
# print(listy)
# return JsonResponse({'a':listy})
#
# URL = a.get("urls1")  # 解析字典，得到URL
# price = a.get("price")
# print(price)
#
# price_dict['price'] = price
# for i in range(10):  # 创建线程列表
#     t = qosthread(i, URL, request.user.email, price)
#     i += 1
#     threads.append(t)
# for t in threads:  # 各个线程开始进行监测
#     t.start()
#     print(t.threadID)
#     time.sleep(1)
#     records.append(QoS_data.objects.filter(user=request.user).latest('add_time'))  # 各个web服务对应的最新QOS数据
#
