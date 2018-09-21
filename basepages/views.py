from django.shortcuts import render
from users.models import User

from django.http import JsonResponse,HttpResponse
from django.conf import settings
from django.core.mail import send_mail

import json

# Create your views here.
def basepage(request):
    return render(request,'baseframe.html')

def accounts_profile(request):
    if request.method=='POST':
        a=json.loads(request.body)
        print(a)
        b=User.objects.get(email=request.user.email)
        b.name=a['name']
        b.sex = a['sex']
        b.birthday = a['birthday']
        b.job = a['job']
        b.job_city = a['job_city']
        b.join_job_date= a['join_job_date']
        b.xueli = a['xueli']
        b.collage = a['collage']
        b.graduate_date = a['graduate_date']
        b.save()
    return render(request,'accounts_profile.html')


# 发送邮件
def send(request):
    msg='<a href="http://www.baidu.com" target="_blank">点击激活</a>'
    send_mail('测试邮件',
    '',
    settings.EMAIL_FROM,
    ['收件箱'],
    html_message=msg)
    return HttpResponse('ok')

def bootemp(request):
    return render(request,'bootemp.html')