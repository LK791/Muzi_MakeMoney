
'''
总结我实现了什么
那就是,学会了如何在Backtrader里 增加额外的列,
但是发现,其实这样没有必要,
看了 阿里巴巴商学院的 一个老师的教程
按他的逻辑,其实更多的处理,应该在pandas里完成,输入给Backtrader的内容
就应该,只是一个信号
把Backtrader封装成一个黑盒子一样的东西即可
'''

import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
from MyTT import *
import backtrader as bt  # 导入 Backtrader

from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo




# 设置输出右对齐
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有的列
pd.set_option('expand_frame_repr', False)
# 最多显示数据的行数
pd.set_option('display.max_rows', 5000)
# 取消科学计数法,显示完整,可调整小数点后显示位数
# pd.set_option('display.float_format', '{:.2f}'.format)


########################################################################################################################



df = pd.read_csv(
    '/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/第1轮/all_stock_daily_kline_long.csv'
    , index_col=0, parse_dates=['time']  )
# df["time"] = pd.to_datetime(df["time"])
########################################################################################################################


# 获取所有的股票名字列表,unique 就是 去重的意思,不要重复
所有股票名 = df['htsc_code'].unique()
df02 = df[df['htsc_code'] == 所有股票名[0]]

CLOSE = df02.close.values
OPEN = df02.open.values
HIGH = df02.high.values
LOW = df02.low.values
MA5 = MA(CLOSE, 5)
K, D, J = KDJ(CLOSE, HIGH, LOW, N=9, M1=3, M2=3)
# print(K )
#
# print(  )
# exit()
df.loc[df['htsc_code'] == 所有股票名[0] , 'K' ]    =  K

df = df[df['htsc_code'] == 所有股票名[0]]

df= df.fillna(method='bfill')



########################################################################################################################
# 策略部分

class Mystrategy(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        if self.position.size == 0 :
            self.buy(  size=120)
        else :
            self.sell(size=120)




########################################################################################################################

# 定义额外的列 传到进去~~~~








########################################################################################################################
# Backtrader 运行部分


# 实例化 cerebro
cerebro = bt.Cerebro()

# 通过feeds加载数据
data = bt.feeds.PandasData(
    dataname=df    ,
    fromdate=datetime(2019, 1, 1),
    todate=datetime(2021, 1, 1),
    datetime='time',
    open='open',
    high='high',
    low='low',
    close='close',
    volume='volume',
    openinterest= 'K'
)




# 数据传输给大脑
# cerebro.adddata(data, name=所有股票名[0])
cerebro.adddata( data , name = 'shuaiqi'  )

# 加载策略
cerebro.addstrategy(Mystrategy)


# 设置初始资金 100000
cerebro.broker.setcash(880000.0)

# 佣金，双边各 0.0003
cerebro.broker.setcommission(commission=0.0003)

# 滑点：双边各 0.0001
cerebro.broker.set_slippage_perc(perc=0.0001)


# 策略开始运行
result = cerebro.run()


# 输出图
# cerebro.plot()

plotconfig = {
    'id:ind#0': dict(
        subplot=True,
    ),
}
b = Bokeh(style='line', scheme=Tradimo(),plotconfig=plotconfig)
cerebro.plot(b)