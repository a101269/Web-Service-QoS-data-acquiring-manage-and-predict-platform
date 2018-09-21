import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wbqossite.settings")# project_name 项目名称
django.setup()
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.stattools as st
import statsmodels.api as sm
import numpy as np
import pyflux as pf
from get_qos.models import QoS_data
import pandas as pd
import numpy as np
import time,datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data=[]
records=QoS_data.objects.filter(ws_url="https://way.jd.com/QT/airQualityRankquery?city=黔东南州&date=2018-01-16&appkey=8604c9fc84720c85155a6a06770c2683")  # 各个web服务对应的最新QOS数据
for i in range(len(records)):
    data.append(records[i].total_time)
data = pd.DataFrame(data)
print(data)


def plot_acfandpacf(dataset):
    D_data = data
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.graphics.tsaplots import plot_pacf
    fig = plt.figure(figsize=(40,10))
    ax1=fig.add_subplot(211)
    plot_acf(D_data,lags=40,ax=ax1).show()
    ax2=fig.add_subplot(212)
    plot_pacf(D_data,lags=40,ax=ax2).show()
    plt.show()

plot_acfandpacf(data)