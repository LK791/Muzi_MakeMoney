import os.path
import sqlite3
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
from 函数.MyTT import *
from 函数.hanshu001 import *
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
pd.set_option('display.float_format', '{:.2f}'.format)
# todo 自定义函数-------------------------------------
def feed投喂(df ,cerebro ) :
    i =  df['股票代码'].iloc[0]
    df_1  = to_单股处理(i,df)
    data = bt.feeds.PandasData(
        dataname=df_1,
        fromdate=datetime(2019, 1, 2),
        todate=datetime(2023, 2, 16),
        datetime='time',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=0
    )
    cerebro.adddata(data, name=i)
    global a
    a= a+1
    print(  a )
# todo 处理数据-------------------------------------
df = 获取多个df( 40)
股票所有代码 = df['股票代码'].unique()
沪深300_df = pd.read_csv( filepath_or_buffer=r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/hs300.csv'
                            ,parse_dates=['time'])
沪深300_df['time'] = 沪深300_df['time'].dt.date
沪深300_df.set_index('time', inplace=True  )
a = 0
cash_value = {}
# todo 待买处理-------------------------------------
df = df.groupby('股票代码',group_keys=False).apply(lambda x: 指标计算(x))
aa = df.groupby('time',group_keys=False).apply(lambda x: 买点(x))
买清单 = dict(aa)
# todo 策略部分-------------------------------------
class 空策略(bt.Strategy):
    def __init__(self):
        self.buy_list = []
        pass
    def prenext(self):
        self.next()
    def next(self):
        print('-' * 200)
        print( self.datetime.date(0) )
        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        持仓列表 = [aa._name for aa in self.broker.positions if self.broker.getposition(aa).size > 0 ]
        print (  '当前持仓列表' , 持仓列表 )
        if  持仓列表 :
            for i in 持仓列表 :
                self.close( i )
        if  self.datetime.datetime(0) in  list(买清单.keys())    :
            self.buy_list =  list( set(买清单[self.datetime.datetime(0)] )-  set(持仓列表) )
            print( 'buy_list'  , self.buy_list  )
            self.oldlist = 买清单[self.datetime.datetime(0)]
            for i in   self.buy_list  :
                # self.order_target_percent(target=0.95/ len(self.buy_list), data=i)
                self.buy( data=i, size=100)
        else :
            # self.close(   '000002.SZ'  )
            pass
    def log(self, txt ):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        print(  txt  )
    def notify_trade(self, trade):
        # print( self._trades[self.data0][0][-1].dtopen )
        # for i in self._trades[self.data0][0] :
        #     print( i )
        # print( self.trades )
        # print( type(trade) )
        # print( type(self.trade) )
        if trade.isclosed:
            print('股票代码 %s   毛收益 %0.2f, 扣佣后收益 % 0.2f, 佣金 %.2f' %
                ( trade.data._name ,    trade.pnl, trade.pnlcomm, trade.commission))
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
# todo 主程序设置-------------------------------------
cerebro = bt.Cerebro(
    cheat_on_open=True ,    # 开启作弊模式
    stdstats=False          # 禁止观察器,能提升速度
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
# cerebro.run(save_my_data=True)
# 运行程序,加载数据
cerebro.run(load_my_data=True)
# todo 输出结果-------------------------------------
# 资金曲线对齐
沪深300_df['close'] = 沪深300_df['close']/(沪深300_df['close'][0]/2000000)
沪深300_df['close'].plot()
cash_value = pd.Series(cash_value)
cash_value.index = pd.to_datetime(cash_value.index  )
cash_value.plot( )
plt.show()
#系统自带的绘图,多股回测不好用
# cerebro.plot( )
print(         )
end_time = time.time()
execution_time = end_time - start_time
print("运行时间：", execution_time, "秒")
exit()
