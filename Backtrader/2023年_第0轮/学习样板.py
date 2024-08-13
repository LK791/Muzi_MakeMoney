import backtrader as bt
import pandas as pd

from com.insight import common
from com.insight.query import *
from com.insight.market_service import market_service

from datetime import datetime


exit()


# user 用户名
# password 密码
def login():
    # 登陆前 初始化
    user = ""       #请填入自己的用户名
    password = ""   #请填入自己的密码
    common.login(market_service, user, password)

class Mystrategy(bt.Strategy):
    def __init__(self):
        pass

    def start(self):
        print("start")

    def prenext(self):
        print("prenext")

    def next(self):
        print("next")


if __name__ == '__main__':
    #方法一
    # login()
    # df = get_kline(htsc_code=["601688.SH"], time=[datetime(2021, 5, 10), datetime(2022, 5, 10)],
    #                    frequency="daily", fq="none")
    # csv = df.to_csv("daily-kline.csv")
    #方法二
    df = pd.read_csv("daily-kline.csv")
    df["time"] = pd.to_datetime(df["time"])

    data = bt.feeds.PandasData(
        dataname=df,
        fromdate=datetime(2021, 5, 10),
        todate=datetime(2022, 5, 10),
        datetime='time',
        # open='open',
        # high='high',
        # low='low',
        # close='close',
        # volume='volume',
        openinterest=-1
    )
    cerebro = bt.Cerebro()
    cerebro.adddata(data, name="daily_kline")
    cerebro.addstrategy(Mystrategy)
    result = cerebro.run()

    cerebro.plot()
