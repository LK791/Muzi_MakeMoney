import sqlite3
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
from MyTT import *
from Backtrader.第1轮.函数.hanshu001 import *
import backtrader as bt  # 导入 Backtrader
import matplotlib.pyplot as plt
import talib
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




##########################################################################

# 获取已经处理时间
# df = 获取单个df()

df = 获取多个df(5)
股票所有代码 = df['股票代码'].unique()


# print(   df[df['股票代码']== '000007.SZ'] )
# end_time = time.time()
# execution_time = end_time - start_time
# print("运行时间：", execution_time, "秒")
# exit()



# 策略

class celue000(bt.Strategy):
    # 全局设定交易策略的参数
    def log(self, txt ):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        print(  txt  )



    def __init__(self):
        pass

    def prenext(self):
        self.next()

    def next(self):
        print('-'*200)
        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        print(self.datetime.date(0))
        print(  '今天的开盘价:   ' +  str(self.data.open[0]))
        print(  '今天的收盘价:   ' +  str(self.data.close[0]))
        if  str(self.datetime.date(0)) == '2020-02-18':
            print('提交订单')
            self.buy(  size=120)
            self.buy( data = '000007.SZ' , size=4000)
        if str(self.datetime.date(0)) == '2020-02-26':

            self.sell(data='000007.SZ', size=4000)
            self.sell(size=120)


        print('当前持仓如下:' )
        # print( self.position(self.datas[0]) )
        # print( self.getposition( self.datas[0] ) )
        # hold_bond_name = []
        # for   _p in self.broker.positions:
        #     # if self.broker.getposition(_p).size >= 0:
        #     #     hold_bond_name.append(_p._name)
        #         print(  _p._name   ,   self.getposition(_p).size  ,self.getposition(_p).price )
        posdata = [d for d, pos in self.getpositions().items() if pos.size > 0 ]
        for i in  posdata :
            abc = self.getposition(i )
            print( i._name ,
                    '单笔盈利:', round((abc.adjbase-abc.price)*abc.size ,2) ,
                    '当前货值', round(abc.adjbase * abc.size, 2),
                    '成本价格',round(abc.price,2),
                    '现在价格',round(abc.adjbase,2)
                    )

        print('账户总资产:',round(self.broker.getvalue(),2),'剩余的钱:',self.broker.getcash())
        print()

    def notify_order(self, order):
        # 未被处理的订单
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 已经处理的订单
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                print("订单尾盘成交:", self.data.num2date(order.executed.dt).date())
                self.log(
                    '尾盘购买成功,Stock: %s , ref:%.0f，成交价格: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f ' %
                    (order.data._name,# 股票名称
                    order.ref,  # 订单编号
                    order.executed.price,  # 成交价
                    order.executed.value,  # 成交额
                    order.executed.comm,  # 佣金
                    order.executed.size,  # 成交量

                    ))
            else: # Sell
                print("订单尾盘成交:", self.data.num2date(order.executed.dt).date())
                self.log('尾盘卖出成功, Stock: %s , ref:%.0f, 成交价格: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f , ' %
                        (order.data._name,
                        order.ref,
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                        order.executed.size,

                        ))


class celue001(bt.Strategy):
    # 全局设定交易策略的参数

    def __init__(self):
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.list = []
        self.oldlist = []
    def next(self):
    # def next_open(self):
        # 检查是否持仓

        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        时间戳 = self.datas[0].datetime.datetime(0)
        print('帅气的凯子哥今天待买的股票如下:' )
        print(时间戳 )
        print(buy_date[时间戳])

        if self.oldlist:
            for i in self.oldlist:
                self.order_target_percent(target=0, data=i)
            self.oldlist = []


        if 时间戳  in buy_date.keys():
            self.list = buy_date[时间戳]
            self.oldlist = buy_date[时间戳]
            for i in self.list:
                self.order_target_percent(target=0.9 / len(self.list), data=i)

    def log(self, txt, dt=None):
        ''' 输出日志'''
        dt = dt or self.datas[0].datetime.date(0)  # 拿现在的日期
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(f"""买入{order.data._name}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            elif order.issell():
                self.log(f"""卖出{order.data._name}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None




# cerebro = bt.Cerebro()
cerebro = bt.Cerebro(cheat_on_open=True , stdstats=False) # 作弊模式打开
cerebro.broker.set_coc(True)  # 设置以当日收盘价成交


for i  in  股票所有代码:
    df_1 = to_单股处理(i,df)
    data = bt.feeds.PandasData(
        dataname = df_1,
        fromdate = datetime(2018, 1, 2),
        todate=datetime(2023, 2, 17),
        datetime='time',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )
    cerebro.adddata(data, name=i)

cerebro.broker.setcash(1000000.0)# 设置初始资金
cash_value = {}
# 添加策略
cerebro.addstrategy(celue000)


# 添加观察器
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')



results = cerebro.run()

strat = results[0]
print('最终资金: %.2f' % cerebro.broker.getvalue())
print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis()['sharperatio'])
print('回撤指标:', strat.analyzers.DW.get_analysis())

# cash_value = pd.Series(cash_value)
# cash_value.plot(figsize=(18,6))
# plt.show()

# 输出图
# cerebro.plot()
# cerebro.plot(iplot=False, volume=False, subplot=False)

