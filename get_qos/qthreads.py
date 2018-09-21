from threading import Thread
from get_qos.models import QoS_data
from users.models import User
from get_qos.models import Monitor
from io import BytesIO
import pycurl
import sys
import time

class qthread(Thread):
    def __init__(self, threadID,URL,email,price,endtime,internal):
        Thread.__init__(self)
        self.threadID = threadID
        self.URL = URL
        self.email=email
        self.price=price
        self.endtime=endtime
        self.internal=internal
    def run(self):
        getqos(self.URL, self.email,self.price,self.endtime,self.internal)

def getqos(URL,email,price,endtime,internal):
    time_passed=0
    URL = URL.encode('utf-8')
    curl = pycurl.Curl()  # 创建一个Curl对象
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.setopt(pycurl.URL, URL)  # 定义请求的URL常量
    curl.setopt(pycurl.ENCODING, 'gzip,deflate')
    curl.setopt(pycurl.CONNECTTIMEOUT, 10)  # 定义请求连接的等待时间
    curl.setopt(pycurl.TIMEOUT, 10)  # 定义请求超时时间
    curl.setopt(pycurl.NOPROGRESS, 1)  # 屏蔽下载进度条
    curl.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
    curl.setopt(pycurl.MAXREDIRS, 1)  # 指定HTTP重定向的最大数为1
    curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)  # 设置保存DNS信息的时间为30秒
    buff = BytesIO()
    curl.setopt(pycurl.WRITEFUNCTION, buff.write)  # pycurl模块不具备存储的功能，所以将数据写入字节流当中
    while(True):
        try:
            curl.perform()  # 提交请求
        except Exception as e:
            print("connecion error:" + str(e))
            buff.close()
            curl.close()
            sys.exit()

        # RESP0NSE_WORDS = buff.getvalue().decode("utf-8")
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

        u = User.objects.get(email=email)
        qosdata = QoS_data(ws_url=URL,http_code=HTTP_CODE, total_time=TOTAL_TIME, size_download=SIZE_DOWNLOAD,namelookup_time=NAMELOOKUP_TIME,
                           connect_time=CONNECT_TIME,pretransfer_time=PRETRANSFER_TIME,starttransfer_time=STARTTRANSFER_TIME,redirect_time=REDIRECT_TIME,
                           size_upload=SIZE_UPLOAD,header_size=HEADER_SIZE,speed_download=SPEED_DOWNLOAD,speed_upload=SPEED_UPLOAD,price=price)
        qosdata.save()
        qosdata.user.add(u)  # cannot access related objects of a many-to-many relation before the instance is saved


        time.sleep(internal)
        time_passed += internal
        if time_passed>endtime:
            break
    buff.close()
    curl.close()  # 关闭Curl对象
    out = Monitor.objects.get(ws_url=URL)
    out.is_monitor = 0
    out.save()
    print("tast over!!!!!!")


