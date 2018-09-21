from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import os
import sys
sys.path.append('F:\\PycharmProjects\wbqossite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wbqossite.settings")# project_name 项目名称
import django
django.setup()
from get_qos.qthreads import qthread
from get_qos.models import Example_base

@shared_task(track_started=True)
def add(x,y):
    print("hello")
    # time.sleep(30)  # 模拟长时间执行
    case = Example_base(type="计算askdjaks", bandwidth=x, workload=y, qos_time=250)
    case.save()


@shared_task(track_started=True)
def monitor(urls,total_time,email,time_internal):
    threads = []
    i=0
    print(email)
    print(total_time)
    for ws in urls:     #创建线程列
        t = qthread(i, ws, email, 0, total_time, time_internal)
        i+=1
        threads.append(t)
    for t in threads:  # 各个线程开始进行监测?
        t.start()
        print(t.threadID)
    print("Good bye!")
    return email


