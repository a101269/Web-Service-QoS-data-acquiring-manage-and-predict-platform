from threading import Thread
from get_qos.models import QoS_datacaiji
from users.models import User
from io import BytesIO
import pycurl
import sys

class qosthread(Thread):
    def __init__(self, threadID,URL,email,price):
        Thread.__init__(self)
        self.threadID = threadID
        self.URL = URL
        self.email=email
        self.price=price
    def run(self):
        getdata(self.URL, self.email,self.price)

def getdata(URL,email,price):
    URL = URL.encode('utf-8')
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


    # con = response_dict.get("RESP0NSE_WORDS")
    # print("返回内容：%s" % con)

    # if 'HTTP_X_FORWARDED_FOR' in request.META:
    #     ip = request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']

        # 数据保存至数据库
    u = User.objects.get(email=email)
    qosdata = QoS_datacaiji(ws_url=URL,http_code=HTTP_CODE, total_time=TOTAL_TIME, size_download=SIZE_DOWNLOAD,namelookup_time=NAMELOOKUP_TIME,
                       connect_time=CONNECT_TIME,pretransfer_time=PRETRANSFER_TIME,starttransfer_time=STARTTRANSFER_TIME,redirect_time=REDIRECT_TIME,
                       size_upload=SIZE_UPLOAD,header_size=HEADER_SIZE,speed_download=SPEED_DOWNLOAD,speed_upload=SPEED_UPLOAD,price=price)
    qosdata.save()
    qosdata.user.add(u)  # cannot access related objects of a many-to-many relation before the instance is saved

    # 打印输出相关数据
    # print("返回内容：%s" % RESP0NSE_WORDS)
    # print("HTTP状态码：%s" % (HTTP_CODE))
    # print("DNS解析时间：%.2f us" % (NAMELOOKUP_TIME))
    # print("建立连接时间：%.2f ms" % (CONNECT_TIME))
    # print("准备传输时间：%.2f ms" % (PRETRANSFER_TIME))
    # print("传输开始时间：%.2f ms" % (STARTTRANSFER_TIME))
    # print("传输结束总时间：%.2f ms" % (TOTAL_TIME))
    # print("重定向所消耗时间：%.2f us" % (REDIRECT_TIME))
    # print("HTTP头部大小：%d byte" % (HEADER_SIZE))
    # print("下载数据包大小：%d bytes/s" % (SIZE_DOWNLOAD))
    # print("上传数据包大小：%d bytes/s" % (SIZE_UPLOAD))
    # print("平均下载速度：%d bytes/s" % (SPEED_DOWNLOAD))
    # print("平均上传速度：%d bytes/s" % (SPEED_UPLOAD))

    buff.close()
    curl.close()        # 关闭Curl对象
    return TOTAL_TIME
