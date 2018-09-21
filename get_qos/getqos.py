# -*- coding: utf-8 -*-
from io import BytesIO
import sys
import pycurl

# URL = "https://way.jd.com/he/freeweather?city=beijing&appkey=8604c9fc84720c85155a6a06770c2683"# 目标web服务接口URL
URL="https://way.jd.com/jisuapi/get?channel=头条&num=10&start=0&appkey=8604c9fc84720c85155a6a06770c2683".encode('utf-8')
# URL="https://way.jd.com/jisuapi/search?keyword=白菜&num=10&appkey=8604c9fc84720c85155a6a06770c2683".encode('utf-8')
c = pycurl.Curl() # 创建Curl对象
c.setopt(pycurl.SSL_VERIFYPEER, 0)
c.setopt(pycurl.SSL_VERIFYHOST, 0)
c.setopt(pycurl.URL, URL)# 定义请求的URL常量
c.setopt(pycurl.ENCODING,'gzip,deflate')
c.setopt(pycurl.CONNECTTIMEOUT, 5)# 定义请求连接的等待时间
c.setopt(pycurl.TIMEOUT, 5)# 定义请求超时时间
c.setopt(pycurl.NOPROGRESS, 1)# 屏蔽下载进度条
c.setopt(pycurl.FORBID_REUSE, 1)# 完成交互后强制断开连接，不重用
c.setopt(pycurl.MAXREDIRS, 1)# 指定HTTP重定向的最大数为1
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)# 设置保存DNS信息的时间为30秒
# indexfile = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")# 创建一个文件对象，以“wb”方式打开，用来存储返回的http头部及页面内容
# c.setopt(pycurl.WRITEHEADER, indexfile)# 将返回的HTTP HEADER定向到indexfile文件
# c.setopt(pycurl.WRITEDATA, indexfile)# 将返回的HTML内容定向到indexfile文件对象
buff = BytesIO()
c.setopt(pycurl.WRITEFUNCTION, buff.write) #pycurl模块不具备存储的功能，所以将数据写入字节流当中

try:
    c.perform()  # 提交请求
except Exception as e:
    print("connecion error:" + str(e))
    # indexfile.close()
    c.close()
    sys.exit()

NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)# DNS解析时间
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)# 建立连接时间
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)# 从建立连接到准备传输所消耗的时间
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)# 从建立连接到传输开始消耗的时间
REDIRECT_TIME= c.getinfo(c.REDIRECT_TIME)# 重定向所消耗的时间
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)# 传输的总时间
HTTP_CODE = c.getinfo(c.HTTP_CODE)# HTTP状态码
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)# 下载数据包大小
SIZE_UPLOAD = c.getinfo(c.SIZE_UPLOAD)# 上传数据包大小
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)# HTTP头部大小
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)# 平均下载速度
SPEED_UPLOAD= c.getinfo(c.SPEED_UPLOAD)# 平均上传速度

# 打印输出相关数据
# buff.getvalue().decode("utf-8")
print("返回内容：%s" % buff.getvalue().decode("utf-8"))
print("HTTP状态码：%s" % (HTTP_CODE))
print("DNS解析时间：%.2f ms" % (NAMELOOKUP_TIME * 1000))
print("建立连接时间：%.2f ms" % (CONNECT_TIME * 1000))
print("准备传输时间：%.2f ms" % (PRETRANSFER_TIME * 1000))
print("传输开始时间：%.2f ms" % (STARTTRANSFER_TIME * 1000))
print("传输结束总时间：%.2f ms" % (TOTAL_TIME * 1000))
print("重定向所消耗时间：%.2f ms" % (REDIRECT_TIME * 1000))
print("HTTP头部大小：%d byte" % (HEADER_SIZE))
print("下载数据包大小：%d bytes/s" % (SIZE_DOWNLOAD))
print("上传数据包大小：%d bytes/s" % (SIZE_UPLOAD))
print("平均下载速度：%d bytes/s" % (SPEED_DOWNLOAD))
print("平均上传速度：%d bytes/s" % (SPEED_UPLOAD))

# 关闭文件及Curl对象
# indexfile.close()
buff.close()
c.close()