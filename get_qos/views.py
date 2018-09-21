# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse,HttpResponse
from django.db import models
from get_qos.models import QoS_data
from get_qos.models import QoS_attributes
from get_qos.models import Monitor
from get_qos.models import Monitor_setting
from get_qos.models import Example_base
from get_qos.models import Notice
from users.models import User
from get_qos.getqos_threads import qosthread
from threading import Thread
from io import BytesIO
import numpy as np
import json
import pycurl
import sys
import time
from get_qos.models import QoS_datacaiji
import subprocess
from get_qos.test import add
from get_qos.test import monitor

# Create your views here.
def t(request):
    return render(request,'ttexy.html')

def attributes_choose(request):
    return render(request,'attributes_choose.html')

def attributes_setting(request):
    if request.method == "POST":
        # v = request.POST.getlist('to')   #以下设置要清洗的数据
        # attrs_list = [1,2,3,4,5,6,7,8,9,10,11,12]
        # for j in attrs_list:
        #     attr_n = QoS_attributes.objects.get(number=j)
        #     attr_n.is_collect =0
        #     attr_n.save()
        # for i in v:
        #     attr_y = QoS_attributes.objects.get(number=i)
        #     print(attr_y.number)
        #     attr_y.is_collect=1
        #     attr_y.save()
        interval = request.POST.get('interval')   #以下设置监测时间间隔
        total_days = request.POST.get('total_time')   #以下设置监测时间间隔
        inter = Monitor_setting.objects.filter(user=request.user)
        if inter.exists():
            for i in inter:
                i.time_interval=interval
                i.total_time=total_days
                i.save()
        else:
            u = User.objects.get(email=request.user.email)
            setting = Monitor_setting(time_interval=interval,total_time=total_days)
            setting.save()
            setting.user.add(u)
    return render(request, 'attributes_setting.html')

def monitor_setting(request):
    if request.method == "POST":
        interval = request.POST.get('interval')   #以下设置监测时间间隔
        total_days = request.POST.get('total_time')   #以下设置监测时间间隔
        inter = Monitor_setting.objects.filter(user=request.user)
        if inter.exists():
            for i in inter:
                i.time_interval=interval
                i.total_time=total_days
                i.save()
        else:
            u = User.objects.get(email=request.user.email)
            setting = Monitor_setting(time_interval=interval,total_time=total_days)
            setting.save()
            setting.user.add(u)
    return render(request, 'monitor_setting.html')


def webservice_addurl(request):
    return render(request,'webservice_addurl.html')

def webservice_url(request):
    return render(request, 'webservice_url.html')

def webservice_qos_gatherrrrrrrrrrrrr(request):
    if request.method=='POST':
        a=json.loads(request.body)#将收到url列表由JSON转化为字典
        print(a)
        URL=a.get("urls1")#解析字典，得到URL
        URL=URL.encode('utf-8')
        curl = pycurl.Curl()  # 创建一个Curl对象
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.URL, URL)  # 定义请求的URL常量
        curl.setopt(pycurl.ENCODING,'gzip,deflate')
        curl.setopt(pycurl.CONNECTTIMEOUT, 5)  # 定义请求连接的等待时间
        curl.setopt(pycurl.TIMEOUT, 5)  # 定义请求超时时间
        curl.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条
        curl.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
        curl.setopt(pycurl.MAXREDIRS, 1)  # 指定HTTP重定向的最大数为1
        curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)  # 设置保存DNS信息的时间为30秒
        buff = BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, buff.write)  # pycurl模块不具备存储的功能，所以将数据写入字节流当中
        try:
            curl.perform()  # 提交请求
        except Exception as e:
            print("connecion error:" + str(e))
            buff.close()
            curl.close()
            sys.exit()

        RESP0NSE_WORDS = buff.getvalue().decode("utf-8")
        NAMELOOKUP_TIME = curl.getinfo(curl.NAMELOOKUP_TIME)  # DNS解析时间,单位us
        CONNECT_TIME = curl.getinfo(curl.CONNECT_TIME) * 1000  # 建立连接时间,单位ms
        PRETRANSFER_TIME = curl.getinfo(curl.PRETRANSFER_TIME) * 1000 # 从建立连接到准备传输所消耗的时间,单位ms
        STARTTRANSFER_TIME = curl.getinfo(curl.STARTTRANSFER_TIME) * 1000  # 从建立连接到开始传输消耗的时间,单位ms
        REDIRECT_TIME = curl.getinfo(curl.REDIRECT_TIME)  # 重定向所消耗的时间,单位us
        TOTAL_TIME = curl.getinfo(curl.TOTAL_TIME) * 1000  # 传输的总时间,单位ms
        HTTP_CODE = curl.getinfo(curl.HTTP_CODE)  # HTTP状态码
        SIZE_DOWNLOAD = curl.getinfo(curl.SIZE_DOWNLOAD)  # 下载数据包大小
        SIZE_UPLOAD = curl.getinfo(curl.SIZE_UPLOAD)  # 上传数据包大小
        HEADER_SIZE = curl.getinfo(curl.HEADER_SIZE)  # HTTP头部大小
        SPEED_DOWNLOAD = curl.getinfo(curl.SPEED_DOWNLOAD)  # 平均下载速度
        SPEED_UPLOAD = curl.getinfo(curl.SPEED_UPLOAD)  # 平均上传速度

        global response_dict
        response_dict = {'RESP0NSE_WORDS': RESP0NSE_WORDS, 'HTTP_CODE': HTTP_CODE,'TOTAL_TIME':TOTAL_TIME} #要显示在HTML中的数据保存在字典中
        # con = response_dict.get("RESP0NSE_WORDS")
        # print("返回内容：%s" % con)

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

            # 数据保存至数据库
        u = User.objects.get(email=request.user.email)
        qosdata = QoS_data(ws_url=URL,http_code=HTTP_CODE, tltal_time=TOTAL_TIME, size_download=SIZE_DOWNLOAD,user_ip=ip)
        qosdata.save()
        qosdata.user.add(u)  # cannot access related objects of a many-to-many relation before the instance is saved

        # 打印输出相关数据
        # print("返回内容：%s" % RESP0NSE_WORDS)
        print("HTTP状态码：%s" % (HTTP_CODE))
        print("DNS解析时间：%.2f us" % (NAMELOOKUP_TIME))
        print("建立连接时间：%.2f ms" % (CONNECT_TIME))
        print("准备传输时间：%.2f ms" % (PRETRANSFER_TIME))
        print("传输开始时间：%.2f ms" % (STARTTRANSFER_TIME))
        print("传输结束总时间：%.2f ms" % (TOTAL_TIME))
        print("重定向所消耗时间：%.2f us" % (REDIRECT_TIME))
        print("HTTP头部大小：%d byte" % (HEADER_SIZE))
        print("下载数据包大小：%d bytes/s" % (SIZE_DOWNLOAD))
        print("上传数据包大小：%d bytes/s" % (SIZE_UPLOAD))
        print("平均下载速度：%d bytes/s" % (SPEED_DOWNLOAD))
        print("平均上传速度：%d bytes/s" % (SPEED_UPLOAD))

        buff.close()
        curl.close()        # 关闭Curl对象
    return render(request,'webservice_qosdata.html', {'response_dict': response_dict})

def monitor_list(request):
    if request.method == "POST":
        v = request.POST.getlist('address')
        t = request.POST.getlist('tag')
        i=0
        for i in range(len(v)):
            u = User.objects.get(email=request.user.email)
            addr = Monitor(ws_url=v[i])
            addr.tag=t[i]
            addr.save()
            addr.user.add(u)
    ws_list = Monitor.objects.filter(user=request.user)
    # print(url_list)
    return render(request, 'monitor_list.html',{'ws_list': ws_list})

@csrf_exempt
def monitor_addel(request):
    urls = []
    if request.method == "POST":
        a=request.POST
        print(a)
        yearry = json.loads(a.get("yearry"))
        noarry = json.loads(a.get("noarry"))
        dearry = json.loads(a.get("dearry"))
        # yearry = a.get("yearry")  # 解析字典
        # print(yearry)
        # for n in yearry:
        #     print(n)
        for j in yearry:
            join = Monitor.objects.get(id=j)
            join.is_monitor=1
            join.save()
            urls.append(join.ws_url)
        time_inter = Monitor_setting.objects.get(user=request.user)
        time_internal = time_inter.time_interval*60  # 监测周期
        total_days = time_inter.total_time*86400  # 监测天数
        email = request.user.email
        print(time_internal)
        print(total_days)
        monitor.delay(urls, total_days, email,time_internal)
        for k in noarry:
            out = Monitor.objects.get(id=k)
            out.is_monitor=0
            out.save()
        for h in dearry:
            d = Monitor.objects.get(id=h)
            d.delete()
        return render(request, 'monitor_list.html')

@csrf_exempt
def monitoring(request):
    tags = []
    monitoring_list = Monitor.objects.filter(user=request.user,is_monitor=1)
    for ws in monitoring_list:
        tags.append(ws.tag)
    print(tags[0]) #web服务标签
    if len(tags)<5:
        for num in range(len(tags), 5):
            tags.append('null')
    time_inter=Monitor_setting.objects.get(id=1)
    time_internal=time_inter.time_interval  #监测周期
    global tag_time
    tag_time = {'t': time_internal,'tag1':tags[0],'tag2':tags[1],'tag3':tags[2],'tag4':tags[3],'tag5':tags[4]}
    return render(request,'monitoring.html',{"tagtime":tag_time})


@csrf_exempt
def monitoring_response(request):
    threads = []
    i=0
    monitoring_list = Monitor.objects.filter(user=request.user,is_monitor=1)
    n=len(monitoring_list)
    records=[]
    listy=[]
    for ws in monitoring_list:     #创建线程列
        t = qosthread(i,ws.ws_url,request.user.email,0)
        i+=1
        threads.append(t)
    for t in threads:#各个线程开始进行监测?
        t.start()
        print(t.threadID)
    for ws in monitoring_list:     #创建线程列表
        records.append(QoS_data.objects.filter(user=request.user, ws_url=ws.ws_url).latest('add_time'))  # 各个web服务对应的最新QOS数据
    for m in range(n):
        listy.append(records[m].total_time)
    print(listy)
    return JsonResponse({'a':listy})

@csrf_exempt
def timeinternal_response(request):
    time_inter=Monitor_setting.objects.get(id=1)
    time_internal=time_inter.time_interval
    # print(time_internal)
    return JsonResponse({'t':time_internal})


@csrf_exempt
def epbase_manage(request):
    if request.method == "POST":
        types = request.POST.getlist('types')
        bandwidth = request.POST.getlist('bandwidth')
        workload = request.POST.getlist('workload')
        qos_time = request.POST.getlist('qos')
        for i in range(len(types)):
            case = Example_base(type=types[i], bandwidth=bandwidth[i],workload=workload[i],qos_time=qos_time[i])
            case.save()
    return render(request,'examplebase_magage.html')

def predict_input(request):
    return render(request, 'qos_predict.html')

def predict_result(request):
    return render(request,'predict_result.html')

@csrf_exempt
def predict(request):
    loads = []
    speeds = []
    qos = []
    sim = []
    sim1 = []
    sim2 = []
    sum_sim = 0
    qos_pre = 0
    qos_five= []
    u=0.6
    v=0.4
    if request.method == "POST":
        a = request.POST
        print(a)
        type = a.get("type")
        # print(type)
        bandwidth = json.loads(a.get("bandwidth"))
        workload = json.loads(a.get("workload"))
        # print(bandwidth)
        cases = Example_base.objects.filter(type=type)
        for i in range(len(cases)):
            loads.append(cases[i].workload)
            speeds.append(cases[i].bandwidth)
            qos.append(cases[i].qos_time)
        # print(loads)
        # print(speeds)
        load_max=max(loads)
        speeds_max=max(speeds)
        for j in range(len(cases)):
            sim1.append(1 - abs((workload - cases[j].workload)/load_max))
            sim2.append(1 - abs((bandwidth - cases[j].bandwidth)/speeds_max))
            sim.append((u*sim1[j]+v*sim2[j])/(u+v))
        print(sim)
        K = 5
        a = np.array(sim)
        a = a[np.argpartition(a,-K)[-K:]]#选择出相似度最大的K个值
        # print(sim_maxarray [1])
        print(a[np.argpartition(a , -K)[-K:]])
        b=min(a)
        c = np.arange(len(sim))  # 生成和sim相同长度的数组
        d = c[sim >= b]  # d存放的就是相似度最大的元素对应的索引
        print(d)
        for n in range(K):
            sum_sim += sim[d[n]]
        for n in range(K):
            print(qos[d[n]])
            qos_five.append(qos[d[n]])
            qos_pre+=((sim[d[n]]/sum_sim)*qos[d[n]])
        print(qos_pre)
        global sim_dict
        sim_dict = {'sim1':sim1,'sim2':sim2,'sim':sim,'sim_five':a,'qos_pre':qos_pre,'qos_five':qos_five}
    return render(request,'predict_result.html',{'sim_dict':sim_dict})

@csrf_exempt
def announcement_release(request):
    return render(request, 'announcement_release.html')

def announcement_save(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        title = a.get("title")
        content = a.get("content")
        # title = json.loads(a.get("title"))
        # content = json.loads(a.get("content"))
        print(title)
        print(content)
        u = User.objects.get(email=request.user.email)
        notice = Notice(title=title,content=content)
        notice.save()
        notice.user.add(u)
    return render(request, 'announcement_release.html')

def announcement_list(request,page):
    notice_list = Notice.objects.all()
    paginator = Paginator(notice_list,4)
    print(notice_list)
    try:
        # 尝试获取请求的页数的信息
        wss = paginator.page(int(page))
    except PageNotAnInteger:
        wss = paginator.page(1)
    except EmptyPage:
        wss = paginator.page(paginator.num_pages)
    return render(request, 'announcement_list.html', {'ws_list':wss})


def announcement_content(request,id):
    print(id)
    content = Notice.objects.get(id=id)
    return render(request, 'announcement_content.html',{'content':content})

@csrf_exempt
def webservice_qos_gather(request):
    if request.method=='POST':
        threads = []
        records = []
        fail_num = 0
        total_time = []
        attri_name = []
        attri_data = []
        price_dict = {}
        # average_time = 0
        a=json.loads(request.body)#将收到url列表由JSON转化为字典
        print(a)
        URL=a.get("urls1")#解析字典，得到URL
        price=a.get("price")
        print(price)
        # URL=URL.encode('utf-8')
        price_dict['price']=price
        for i in range(10):     #创建线程列表
            t = qosthread(i,URL,request.user.email,price)
            i+=1
            threads.append(t)
        for t in threads:#各个线程开始进行监测
            t.start()
            print(t.threadID)
            time.sleep(1)
            records.append(QoS_datacaiji.objects.filter(user=request.user).latest('add_time'))  # 各个web服务对应的最新QOS数据
        for m in range(10):
            total_time.append(records[m].total_time)
            if records[m].http_code != "200":
                fail_num+=1
        average_time=sum(total_time)/10
        print("平均")
        print(average_time)
        fail_ratio = fail_num / 10
        succ_ratio = 1-fail_ratio
        print("出错率")
        print(fail_ratio)

        attributes = QoS_attributes.objects.filter(is_collect=1)
        for k in range(len(attributes)):
            attri_name.append(attributes[k].meaning)
            attri_data.append(QoS_data.objects.values(attri_name[k]).last())
        print(attri_data)
        print(attri_name)
        global  ratio_dict
        ratio_dict = {'succ_ratio': succ_ratio, 'fail_ratio': fail_ratio,'attri_data':attri_data,'fail_num':fail_num}
        ratio_dict['price']=QoS_data.objects.last().price
        ratio_dict['average_time']= average_time
        print(ratio_dict)
    return render(request, 'webservice_qosdata.html',{'ratio_dict':ratio_dict})


def collect_form(request):
    return render(request, 'collect_form.html')


@csrf_exempt
def collect_result(request):
    if request.method == 'POST':
        urls = request.POST.getlist('urls')
        price = request.POST.getlist('price')
        n=len(urls)
        if n ==1:
            request.session["url1"] = urls[0]
            request.session["price1"] = price[0]
        elif n==2:
            request.session["url1"] = urls[0]
            request.session["url2"] = urls[1]
            request.session["price1"] = price[0]
            request.session["price2"] = price[1]
        elif n==3:
            request.session["url1"] = urls[0]
            request.session["url2"] = urls[1]
            request.session["url3"] = urls[2]
            request.session["price1"] = price[0]
            request.session["price2"] = price[1]
            request.session["price3"] = price[2]
        print(n)
        request.session["urlnumber"] = n
        # monitoring_list = []
        # monitoring_list.append(request.session.get("url1", default=None))
        # monitoring_list.append(request.session.get("url2", default=None))
        # monitoring_list.append(request.session.get("url3", default=None))
        # print(monitoring_list)
        global info_dict
        info_dict = {'urls': urls, 'price': price}
        print(info_dict)
    return render(request, 'collect_result.html',{'info_dict':info_dict})


@csrf_exempt
def collect_result2(request):
    if request.method == 'POST':
        a=request.POST
        print(a)
        global b,c,d,e,b2,c2,d2,e2
        b = request.POST.getlist('a')
        c = request.POST.getlist('b')
        d = request.POST.getlist('c')
        e = request.POST.getlist('d')
        b2 = request.POST.getlist('a2')
        c2 = request.POST.getlist('b2')
        d2 = request.POST.getlist('c2')
        e2 = request.POST.getlist('d2')
        print(b,c,d,e)
    return render(request, 'collect_result2.html',{'a':b,'b':c,'c':d,'d':e,'a2':b2,'b2':c2,'c2':d2,'d2':e2})


@csrf_exempt
def collect_response(request):
    threads = []
    i=0
    monitoring_list = []
    price_list = []
    n= request.session.get("urlnumber", default=None)
    if n ==1:
        monitoring_list.append(request.session.get("url1", default=None))
        price_list.append(request.session.get("price1", default=None))
    elif n==2:
        monitoring_list.append(request.session.get("url1", default=None))
        monitoring_list.append(request.session.get("url2", default=None))
        price_list.append(request.session.get("price1", default=None))
        price_list.append(request.session.get("price2", default=None))
    else:
        monitoring_list.append(request.session.get("url1", default=None))
        monitoring_list.append(request.session.get("url2", default=None))
        monitoring_list.append(request.session.get("url3", default=None))
        price_list.append(request.session.get("price1", default=None))
        price_list.append(request.session.get("price2", default=None))
        price_list.append(request.session.get("price3", default=None))
    # monitoring_list.pop()
    # price_list.pop()
    print(monitoring_list)
    n=len(monitoring_list)
    print(n)
    records=[]
    listy=[]
    fail_num = []
    tuntu = []
    price = []
    for ws in monitoring_list:     #创建线程列
        print(ws)
        t = qosthread(i,ws,request.user.email, price_list[i])
        i+=1
        threads.append(t)
    for t in threads:#各个线程开始进行监测?
        t.start()
        print(t.threadID)
    for ws in monitoring_list:
        records.append(QoS_datacaiji.objects.filter(user=request.user, ws_url=ws).latest('add_time'))  # 各个web服务对应的最新QOS数据
    for m in range(n):
        listy.append(records[m].total_time)
        tuntu.append(records[m].size_download/records[m].total_time)
        price.append(records[m].price)
        if records[m].http_code != "200":
            fail_num.append(1)
        else:
            fail_num.append(0)
    print(listy)

    return JsonResponse({'a':listy,'b':tuntu,'c':fail_num,'d':price})


# @csrf_exempt
# def monitoring(request):
#     # subprocess.Popen('python F:\PycharmProjects\wbqossite\get_qos\monitoring.py')
#     # subprocess.Popen('python ./monitoring.py',shell=True)
#     monitoring_list = Monitor.objects.filter(user=request.user,is_monitor=1)
#     urls=[]
#     for ws in monitoring_list:     #创建线程列
#         urls.append(ws.ws_url)
#     time_inter = Monitor_setting.objects.get(id=1)
#     time_internal=time_inter.time_interval  #监测周期
#     email=request.user.email
#     global tag_time
#     tag_time = {'t': time_internal}
#     # add.delay(550, 550)
#     monitor.delay(urls,20,email)
#     return render(request,'monitor_list.html',{"tagtime":tag_time})
#     # return render(request,'monitoring.html',{"tagtime":tag_time})


from django.shortcuts import render,HttpResponse
import xlwt
from io import StringIO,BytesIO
import datetime

def output(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=qos_records.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'QOS')
    #1st line
    sheet.write(0,0, 'url')
    sheet.write(0,1, 'http_code')
    sheet.write(0,2, 'namelookup_time')
    sheet.write(0,3, 'connect_time')
    sheet.write(0,4, 'pretransfer_time')
    sheet.write(0,5, 'starttransfer_time')
    sheet.write(0,6, 'redirect_time')
    sheet.write(0,7, 'total_time')
    sheet.write(0,8, 'header_size')
    sheet.write(0,9, 'size_download')
    sheet.write(0,10, 'size_upload')
    sheet.write(0,11, 'speed_download')
    sheet.write(0,12, 'speed_upload')
    sheet.write(0,13, 'add_time')

    excel_row = 1
    activitys = QoS_data.objects.filter(user=request.user)
    for activity in activitys:
        url = activity.ws_url
        http_code = activity.http_code
        namelookup_time = activity.namelookup_time
        connect_time = activity.connect_time
        pretransfer_time = activity.pretransfer_time
        starttransfer_time= activity.starttransfer_time
        redirect_time = activity.redirect_time
        total_time = activity.total_time
        header_size = activity. header_size
        size_download = activity.size_download
        size_upload = activity.size_upload
        speed_download = activity.speed_download
        speed_upload = activity.speed_upload
        add_time = activity.add_time.strftime('%Y-%m-%d %H:%M:%S')


        sheet.write(excel_row, 0, url )
        sheet.write(excel_row, 1, http_code)
        sheet.write(excel_row, 2, namelookup_time)
        sheet.write(excel_row, 3, connect_time)
        sheet.write(excel_row, 4, pretransfer_time)
        sheet.write(excel_row, 5, starttransfer_time)
        sheet.write(excel_row, 6,  redirect_time)
        sheet.write(excel_row, 7,  total_time)
        sheet.write(excel_row, 8,  header_size)
        sheet.write(excel_row, 9,  size_download)
        sheet.write(excel_row, 10, size_upload)
        sheet.write(excel_row, 11, speed_download)
        sheet.write(excel_row, 12, speed_upload)
        sheet.write(excel_row, 13, add_time)
        excel_row += 1

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def down(request):
    return render(request,'record_download.html')