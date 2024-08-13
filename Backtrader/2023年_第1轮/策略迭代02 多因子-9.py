import os.path
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
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
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

df = 获取多个df(2000 )

股票所有代码 = df['股票代码'].unique()


# 打印list(股票所有代码)
# qq()





class Mystrategy(bt.Strategy):

    # 全局设定交易策略的参数
    def __init__(self):
        pass

    # def next(self):
    #     if self.position.size == 0 :
    #         self.buy(  size=120)
    #     else :
    #         self.sell(size=120)
    # def __init__(self):
    #     pass

    def prenext(self):
        self.next()

    def next(self):
        print('-'*200)
        if  self._trades[self.getdatabyname('000004.SZ')][0]   :
            print( '此单开始日期:',    self.data.num2date(self._trades[self.getdatabyname('000004.SZ')][0][-1].dtopen).date() )

        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        print(self.datetime.date(0))
        print(  '今天的开盘价:   ' +  str(self.data1.open[0]))
        print(  '今天的收盘价:   ' +  str(self.data1.close[0]))
        if  self.position.size < 90 :
            print('提交订单')
            self.buy( '000004.SZ', size=10)
            # self.buy( data = '000007.SZ' , size=4000)
        else :
            self.sell( '000004.SZ', size=90)
        # if str(self.datetime.date(0)) == '2020-02-26':
        # #
        #     self.sell(data='000007.SZ', size=4000)
        #     self.sell(size=120)


        print('当前持仓如下:' )
        # print( self.getposition( self.datas[0] ) )
        # hold_bond_name = []
        # print(  self.getdatabyname('000002.SZ').open[0]   )
        # for   _p in self.broker.positions:
        #     if self.broker.getposition(_p).size >= 0:
        #         print(  _p._name   ,   self.getposition(_p).size  ,self.getposition(_p).price )
        posdata = [d for d, pos in self.getpositions().items() if pos.size != 0 ]
        for i in  posdata :
            abc = self.getposition(i )
            print( i._name ,
                    '单笔盈利:', round((abc.adjbase-abc.price)*abc.size ,2) ,
                    '当前货值', round(abc.adjbase * abc.size, 2),
                    '持仓股数',round( abc.size, 2),
                    '成本价格',round(abc.price,2),
                    '现在价格',round(abc.adjbase,2)
                    )
        print()
        print('账户总资产:',round(self.broker.getvalue(),2),'剩余的钱:',round(self.broker.getcash(),2))
        print()


    def log(self, txt ):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        print(  txt  )


    def notify_trade(self, trade):
        print('okokok' )
        # print( self._trades[self.data0][0][-1].dtopen )
        # for i in self._trades[self.data0][0] :
        #     print( i )
        # print( self.trades )
        # print( type(trade) )
        # print( type(self.trade) )


        if trade.isclosed:
            print('毛收益 %0.2f, 扣佣后收益 % 0.2f, 佣金 %.2f' %
                (trade.pnl, trade.pnlcomm, trade.commission))

    def notify_order(self, order):
        # 未被处理的订单
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 已经处理的订单
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                print("订单成交:", self.data.num2date(order.executed.dt).date())
                self.log(
                    '购买成功,股票名称: %s , 订单编号:%.0f，成交价格: %.2f, 成交额: %.2f, 佣金 %.2f, 成交量: %.2f ' %
                    (order.data._name,# 股票名称
                    order.ref,  # 订单编号
                    order.executed.price,  # 成交价
                    order.executed.value,  # 成交额
                    order.executed.comm,  # 佣金
                    order.executed.size,  # 成交量
                    ))

            else: # Sell
                print("订单成交:", self.data.num2date(order.executed.dt).date())
                self.log('卖出成功, 股票名称: %s , 订单编号:%.0f, 成交价格: %.2f, 成交额: %.2f, 佣金 %.2f, 成交量: %.2f , ' %
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
class Mystrategy1(bt.Strategy):
    def __init__(self):
        pass

    def next(self):
        if self.position.size == 0 :
            self.buy(  size=120)
        else :
            self.sell(size=120)
# cerebro = bt.Cerebro(  )
cerebro = bt.Cerebro(cheat_on_open=True , stdstats=False) # 作弊模式打开
cerebro.broker.set_coc(True)  # 设置以当日收盘价成交

# 开始投喂feeddata
a = 0
# for i  in  股票所有代码:
#     df_1 = to_单股处理(i,df)
#     data = bt.feeds.PandasData(
#         dataname = df_1,
#         fromdate = datetime(2018, 1, 2),
#         todate=datetime(2023, 2, 17),
#         datetime='time',
#         open='open',
#         high='high',
#         low='low',
#         close='close',
#         volume='volume',
#         openinterest=-1
#     )
#     cerebro.adddata(data, name=i)
#     a= a+1
#     print(  a )

def feed投喂(df ,cerebro ) :
    i =  df['股票代码'].iloc[0]
    df_1  = to_单股处理(i,df)
    data = bt.feeds.PandasData(
        dataname=df_1,
        fromdate=datetime(2018, 1, 2),
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
    global a
    a= a+1
    print(  a )
#
df = df.groupby('股票代码',group_keys=False).apply(lambda df : feed投喂(df ,cerebro ))





cerebro.broker.setcash(2000000.0)# 设置初始资金
cash_value = {}

# 添加策略
cerebro.addstrategy(Mystrategy)
# cerebro.addstrategy(Mystrategy)
# 添加观察器



# cerebro.run( )
# cerebro.run(save_my_data=True)
cerebro.run(load_my_data=True)

# cerebro.run(load_my_data=True)
# result = cerebro.run()

# strat = results[0]
# print('最终资金: %.2f' % cerebro.broker.getvalue())
# print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis()['sharperatio'])
# print('回撤指标:', strat.analyzers.DW.get_analysis())

# cash_value = pd.Series(cash_value)
# cash_value.plot(figsize=(18,6))
# plt.show()

# 输出图
# cerebro.plot()
# cerebro.plot(iplot=False, volume=False, subplot=False)

print(         )
end_time = time.time()
execution_time = end_time - start_time
print("运行时间：", execution_time, "秒")
exit()

# plotconfig = {
#     'id:ind#0': dict(
#         subplot=True,
#     )
# }
# b = Bokeh(style='line', scheme=Tradimo(),plotconfig=plotconfig)
# cerebro.plot(b)

