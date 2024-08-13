import os.path
import sqlite3
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
from MyTT import *
from Backtrader.第1轮.函数.hanshu001 import *
import matplotlib.pyplot as plt
import time
start_time = time.time()
# 设置输出右对齐
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有的列
pd.set_option('expand_frame_repr', False)
# 最多显示数据的行数
pd.set_option('display.max_rows', 8000)
# 取消科学计数法,显示完整,可调整小数点后显示位数
# pd.set_option('display.float_format', '{:.2f}'.format)
# todo 自定义函数-------------------------------------
def feed投喂(df ,cerebro ) :
    i =  df['股票代码'].iloc[0]
    df_1  = to_单股处理(i,df)
    data = bt.feeds.PandasData(
        dataname=df_1,
        fromdate=datetime(2018, 1, 2),
        todate=datetime(2023, 2, 16),
        datetime='time',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )
    cerebro.adddata(data, name=i)
    global a
    a= a+1
    print(  a )
a = 0
cash_value = {}
# todo 处理数据-------------------------------------
df = 获取多个df(5)
股票所有代码 = df['股票代码'].unique()
# todo 策略部分-------------------------------------
class 空策略(bt.Strategy):
    def __init__(self):
        pass
    def next(self):
        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        if  self.datetime.date(0) < datetime(2019, 1, 1).date():
            self.buy( '000002.SZ', size=10)
        else :
            self.close(   '000002.SZ'  )
# todo 主程序设置-------------------------------------
cerebro = bt.Cerebro(
    cheat_on_open=True ,    # 开启作弊模式
    stdstats=False          # 禁止观察器,提升速度
    )
cerebro.broker.set_coc(True)  # 设置以当日收盘价成交
# 调用投喂函数,开始投喂df
df.groupby('股票代码',group_keys=False).apply(lambda df : feed投喂(df ,cerebro ))
# 设置初始资金
cerebro.broker.setcash(2000000.0)
# 设置佣金比例
cerebro.broker.setcommission(commission=0.002)
# 设置双边滑点
cerebro.broker.set_slippage_perc(perc=0.0001)
# 添加策略
# cerebro.addstrategy(Mystrategy)
cerebro.addstrategy(空策略)
#运行程序,保存数据
cerebro.run(save_my_data=True)
# 运行程序,加载数据
# cerebro.run(load_my_data=True)
# todo 输出结果-------------------------------------
cash_value = pd.Series(cash_value)
cash_value.plot( )
plt.show()
#系统自带的绘图,多股回测不好用
# cerebro.plot( )
print(         )
end_time = time.time()
execution_time = end_time - start_time
print("运行时间：", execution_time, "秒")
exit()
