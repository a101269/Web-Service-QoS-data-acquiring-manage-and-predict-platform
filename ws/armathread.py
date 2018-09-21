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
from ws.models import Arma_resu
from threading import Thread


class qthread(Thread):
    def __init__(self, threadID,URL):
        Thread.__init__(self)
        self.threadID = threadID
        self.URL = URL

    def run(self):
        run_aram(self.URL,5,5)


def test_stationarity(timeseries):
    dftest = adfuller(timeseries, 1,autolag='AIC')# type: tuple
    # print( dftest)
    return dftest[1]  #返回p值


def best_diff(df, maxdiff = 8):
    p_set = {}
    for i in range(0, maxdiff):
        temp = df.copy() #每次循环前，重置
        if i == 0:
            temp['diff'] = temp[temp.columns[1]]
        else:
            temp['diff'] = temp[temp.columns[1]].diff(i)
            temp = temp.drop(temp.iloc[:i].index) #差分后，前几行的数据会变成nan，所以删掉
        pvalue = test_stationarity(temp['diff'])
        p_set[i] = pvalue
        p_df = pd.DataFrame.from_dict(p_set, orient="index")
        p_df.columns = ['p_value']
    i = 0
    global bestdiff
    while i < len(p_df):
        if p_df['p_value'][i]<0.01:
            global bestdiff
            bestdiff = i
            break
        i += 1
    return bestdiff


def produce_diffed_timeseries(df, diffn):
    if diffn != 0:
        df['diff'] = df[df.columns[1]].apply(lambda x:float(x)).diff(diffn)
    else:
        df['diff'] = df[df.columns[1]].apply(lambda x:float(x))
    df.dropna(inplace=True) #差分之后的nan去掉
    return df


def choose_order(ts, maxar, maxma):
    # print(ts)
    x=list(ts)
    # x = [1 if i % 2 == 0 else 6 for i in range(50)]
    # eta = np.random.normal(0, 0.01, 50)
    # x = x + eta
    # print(x)
    # order = st.arma_order_select_ic(ts, maxar, maxma, ic=['aic', 'bic', 'hqic'])
    order = sm.tsa.stattools.arma_order_select_ic(x, ic=['bic'])
    print( order.bic_min_order)

    return order.bic_min_order #返回以BIC准则确定的阶数，是一个tuple类型



def predict_recover(ts, df, diffn): #放入模型进行拟合的数据是经过对数或（和）差分处理的数据，因而拟合得到的预测y值要经过差分和对数还原才可与原观测值比较
    if diffn != 0:
        ts.iloc[0] = ts.iloc[0]+df['log'][-diffn]
        ts = ts.cumsum()
    ts = np.exp(ts)
#    ts.dropna(inplace=True)
    print('还原完成')
    return ts


def run_aram(URL, maxar, maxma, test_size = 1):#  max_ar、max_ma是p、q值的最大备选值。
    data0 = []
    URL = URL.encode('utf-8')
    print(URL)
    records = QoS_data.objects.filter(ws_url=URL)  # 各个web服务对应的最新QOS数据
    if records.exists():
        for i in range(len(records)):
            data0.append(records[i].total_time)
        df = pd.DataFrame(data0)
    # print(df)

        data = df.dropna()
        print("len_data:")
        print(len(data))
        train_size = len(data)-test_size
        print("len_train_size:")
        print(train_size)
        test= data[train_size:]

        data['log'] = np.log(data[data.columns[0]]) #取对数
        #    test_size = int(len(data) * 0.33)
        train= data[:train_size]
        # global diffn
        if test_stationarity(train[train.columns[0]]) < 0.01:
            print('平稳，不需要差分')
            diffn=0
        else:
            diffn = best_diff(train, maxdiff = 8)
            train = produce_diffed_timeseries(train, diffn)
            print("train_size3:")
            print(len(train))
            print('差分阶数为'+str(diffn)+'，已完成差分')
        print('开始进行ARMA拟合')
        # print(train[train.columns[1]])
        # order = choose_order(train[train.columns[1]], maxar, maxma)
        # print('模型的阶数为：'+str(order))
        # _ar = order[0]
        # _ma = order[1]
        # # train = list(train[train.columns[1]])
        # # print(train )
        # model = pf.ARIMA(data=train, ar=7, ma=1, target=None, family=pf.Normal())
        # model.fit("MLE")
        # test_predict = model.predict(test_size)
        # print(test_predict)
        # # test_predict = predict_recover(test_predict, train, diffn)
        # RMSE = np.sqrt(((np.array(test_predict)-np.array(test))**2).sum()/test_size)#RMSE(Root Mean Squared Error，均方根误差)判断一个模型拟合效果
        # print("预测结果为:"+str(test_predict))
        # print("测试集的RMSE为："+str(RMSE))

        x = list(train[train.columns[0]])
        print(x)
        res = sm.tsa.stattools.arma_order_select_ic(x, ic=['bic'])
        print(res.bic_min_order)
        model = sm.tsa.ARMA(x,res.bic_min_order).fit(disp=0)
        print(len(train))
        print(len(data))
        print("diffn:")
        print(diffn)
        test_predict=model.predict(len(train), len(data)-diffn-1)
        test_predict = pd.DataFrame(test_predict)
        print("预测结果：")
        print(test_predict[0][0])
        resu=Arma_resu(url=URL,total_time=test_predict[0][0])
        resu.save()

    else:
        print("无值")
