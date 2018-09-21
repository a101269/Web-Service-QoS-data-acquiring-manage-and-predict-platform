from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ws.models import Webservice
from ws.models import  Collection_list
from get_qos.models import Monitor
from users.models import User
from ws.models import Arma_resu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from get_qos.models import Notice
from ws.armathread import qthread


def ws_register(request):
    number = Webservice.objects.last().number # 各个web服务对应的最新QOS数据
    number=number+1
    return render(request,'ws_register.html',{'number':number})

def info_save(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        number=a.get("number")#解析字典
        name = a.get("name")
        type = a.get("type")
        tag = a.get("tag")
        supplier = a.get("supplier")
        # register_date = a.get("register_date")
        feature = a.get("feature")
        description = a.get("description")
        ws_address = a.get("ws_address")
        request_method = a.get("request_method")
        result_type = a.get("result_type")
        example = a.get("example")
        price = a.get("price")
        input_parameter = a.get("input_parameter")
        return_parameter = a.get("return_parameter")
        print(price)
        u = User.objects.get(email=request.user.email)
        ws_record = Webservice(ws_address=ws_address,number=number, name=name,type=type,tag=tag,supplier=supplier ,feature=feature
                             ,description=description, request_method=request_method , result_type = result_type ,example =example , input_parameter= input_parameter
                             ,price=price,return_parameter=return_parameter)
        ws_record.save()
        ws_record.user.add(u)
    return render(request,'ws_register.html')


def search(request):
    return render(request,'ws_search.html')

def dosearch(request,page):
    q = request.GET.get('q')
    ws_list = Webservice.objects.filter( Q(name__icontains=q) | Q(tag__icontains=q))
    paginator = Paginator(ws_list,4)
    try:
        # 尝试获取请求的页数的信息
        wss = paginator.page(int(page))
    except PageNotAnInteger:
        wss = paginator.page(1)
    except EmptyPage:
        wss = paginator.page(paginator.num_pages)
    return render(request,'search_result.html', {'ws_list':wss})

def ws_info(request,id):
    print(id)
    info = Webservice.objects.get(number=id)
    if Collection_list.objects.filter(number=id,user=request.user):
        did_coll="取消收藏"
    else:
        did_coll="收藏服务"
    print(did_coll)
    if Monitor.objects.filter(ws_url=info.example,user=request.user):
        did_moni="已在监测列表"
    else:
        did_moni="加入监测列表"
    return render(request, 'ws_info.html', {'info': info,'did_coll':did_coll,'did_moni':did_moni})

@csrf_exempt
def collection_del(request):
    urls = []
    if request.method == "POST":
        a=request.POST
        print(a)
        number = json.loads(a.get("number"))
        d = Collection_list.objects.get(number=number)
        d.delete()
        return JsonResponse({'t': 1})

@csrf_exempt
def collection_add(request):
    urls = []
    if request.method == "POST":
        a=request.POST
        print(a)
        number = json.loads(a.get("number"))
        print(number)
        coll_add=Collection_list(number=number)
        u = User.objects.get(email=request.user.email)
        coll_add.save()
        coll_add.user.add(u)
        return JsonResponse({'t': 1})

@csrf_exempt
def moni_add(request):
    urls = []
    if request.method == "POST":
        a=request.POST
        print(a)
        number = json.loads(a.get("number"))
        print(number)
        ws=Webservice.objects.get(number =number )
        address=ws.ws_address
        tag=ws.tag
        u = User.objects.get(email=request.user.email)
        addr = Monitor(ws_url=address,tag =tag)
        addr.save()
        addr.user.add(u)
        return JsonResponse({'t': 1})

def collection_list(request,page):
    ws=[]
    numbers=Collection_list.objects.filter(user=request.user)
    print(numbers)
    print("number over")
    if numbers:
        for n in numbers:
            ws.append(Webservice.objects.get(number=n.number))
        print(ws)
    paginator = Paginator(ws,4)

    try:
        # 尝试获取请求的页数的信息
        wss = paginator.page(int(page))
    except PageNotAnInteger:
        wss = paginator.page(1)
    except EmptyPage:
        wss = paginator.page(paginator.num_pages)
    return render(request,'collect_list.html', {'ws_list':wss})


@csrf_exempt
def recommand_response(request):
    a = request.POST
    name = a.get("name")
    print(name)
    request.session["name"] = name
    return JsonResponse({'a':name})

@csrf_exempt
def recommand_page(request):
    q=request.session.get("name", default=None)
    ws_list = Webservice.objects.filter( Q(name__icontains=q) | Q(tag__icontains=q))
    threads = []
    times=[]
    i=0
    for ws in ws_list:     #创建线程列
        t = qthread(i,ws.example)
        i+=1
        threads.append(t)
    for t in threads:#各个线程开始进行监测?
        t.start()
        print(t.threadID)
    for t in threads:
        t.join()

    resu = Arma_resu.objects.all()
    for ws in resu:
        times.append(ws.total_time)
    little_index=times.index(min(times))
    print(little_index)
    print(resu[little_index].total_time)
    recommand_ws=resu[little_index].url
    print(recommand_ws)
    re_ws=Webservice.objects.get(example=recommand_ws)
    for ws in resu:
        ws.delete()
    return render(request, 'recommand_page.html',{'ws':re_ws})

def home(request):
    notice_list = Notice.objects.all()
    notice_list=notice_list[::-1]#倒序
    return render(request,'home.html',{'notice_list':notice_list})