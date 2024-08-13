import backtrader as bt
import pandas as pd
import numpy as np
import os.path
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import time
开始时间 = time.time()

np.set_printoptions(threshold=np.inf)  # 打印所有数据
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

pd.set_option('display.unicode.east_asian_width', True)# 设置输出右对齐
pd.set_option('expand_frame_repr', False)# 显示所有的列
pd.set_option('display.max_rows', 8000)# 最多显示数据的行数
pd.set_option('display.float_format', '{:.2f}'.format) # 取消科学计数法,显示完整,可调整小数点后显示位数


# todo 定义函数 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def feed投喂(df ,cerebro ) :
    股票名字 =  str(df['股票代码'].iloc[0])
    data = bt.feeds.PandasData(
        dataname=df,
        fromdate=datetime(开始年,开始月,开始日),
        todate=datetime(结束年,结束月,结束日),
        datetime='date',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )
    cerebro.adddata(data, name= 股票名字 )
    global 计数a
    计数a= 计数a+1
    print(  计数a )

def 时间列对齐数据补全(df):
    # 获取所有唯一日期
    unique_dates = sorted(df['date'].unique())

    # 定义一个内部函数，用于处理每只股票的数据
    def process_stock(stock_df):
        # 确保 DataFrame 包含所有日期
        stock_df = stock_df.set_index('date').reindex(unique_dates).reset_index()

        # 使用前一个交易日的数据填充缺失值
        stock_df.ffill(inplace=True)

        # 如果第一个交易日有缺失值，则用后一个交易日数据填充
        stock_df.bfill(inplace=True)

        return stock_df

    # 对每只股票应用处理函数
    processed_dfs = [process_stock(group) for _, group in df.groupby('代码')]

    # 合并所有处理过的 DataFrame
    aligned_df = pd.concat(processed_dfs, ignore_index=True)

    return aligned_df

def 时间列对齐数据补全(df):
    # 定义需要进行填充处理的列
    fill_columns = ['open', 'high', 'low', 'close', 'volume', '代码', '股票代码']

    # 获取所有唯一日期
    unique_dates = sorted(df['date'].unique())

    # 定义一个内部函数，用于处理每只股票的数据
    def process_stock(stock_df):
        # 为需要填充的列进行时间对齐和填充
        stock_df_fill = stock_df.set_index('date')[fill_columns].reindex(unique_dates).ffill().bfill()

        # 保留其他列不变
        stock_df_other = stock_df.set_index('date').reindex(unique_dates)[stock_df.columns.difference(fill_columns + ['date'])]

        # 将填充后的列与其他列合并
        stock_df_combined = pd.concat([stock_df_fill, stock_df_other], axis=1).reset_index()

        return stock_df_combined

    # 对每只股票应用处理函数
    processed_dfs = [process_stock(group) for _, group in df.groupby('代码')]

    # 合并所有处理过的 DataFrame
    aligned_df = pd.concat(processed_dfs, ignore_index=True)

    return aligned_df

def 排序买点处理(df02, str_排序列, n=3):
    buy_date = []
    # df02['正能排序'] = df02['正能量合集'].rank(ascending=True, pct=True)
    # df02['psy排序'] = df02['psy_1'].rank(ascending=False, pct=True)
    # df02['因子合集'] = df02['psy排序'] + df02['正能排序']
    df02 = df02.sort_values(by=str_排序列, ascending=False)
    buy_date = list(df02['股票代码'].values[:n])
    return  buy_date

def 欺骗餐():
    df测试 = pd.DataFrame({
        'open': np.random.rand(100) * 100,
        'high': np.random.rand(100) * 100,
        'low': np.random.rand(100) * 100,
        'close': np.random.rand(100) * 100,
        'volume': np.random.randint(1, 1000, 100)
    }, index=pd.date_range(start='2020-01-01', periods=100, freq='B'))
    return df测试


def 小数2点(num):
    """将数字格式化为两位小数的字符串形式"""
    return "{:.4f}".format(num)

























# todo 数据输入 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

csv路径 = '数据保存/output.csv'
int_读取股票个数 = 1 # 全部导入填 None
采用策略的序号 =  3   # 0 为 基础空策略
初始本金 = 2000
账户总值 = 初始本金
开始年,开始月,开始日 =  2021,1,1
结束年,结束月,结束日 =  2024,5,1
str_排序列     =  '五小于十2.天60势能'
int_排序名次选择  =  3
计数a = 0














# todo 基础准备-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

df = pd.read_csv(csv路径)
df = df[df['代码'].isin(df['代码'].unique()[:int_读取股票个数])]
df['股票代码'] = df.iloc[:, 1].mul(1000000).astype(int).apply('{:06d}'.format)
df.rename(columns={'时间': 'date', '开盘': 'open', '最高': 'high', '最低': 'low', '收盘': 'close', '成交量': 'volume'}, inplace=True)
df['date'] = df['date'].astype(str)
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df = 时间列对齐数据补全(df)
排序买点 = df.groupby('date').apply(lambda x: 排序买点处理(x, str_排序列, int_排序名次选择), include_groups=False)
排序买入清单 = dict(排序买点)
# print(排序买入清单)
























# todo 策略定义--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class 策略000(bt.Strategy):  # 空策略
    def log(self, txt, dt=None):
        ''' 日志记录函数 '''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        # 这里初始化策略参数和指标
        print('采用___空策略')
        pass

    def next(self):
        # 这里编写策略的逻辑，每个新的市场数据到达时调用一次
        # print('-' * 200)
        # print(self.datetime.date(0))
        # print(self.datas[0]._name)
        pass

class 策略001(bt.Strategy):
    def log(self, **kwargs):
        self.log_记录.append(kwargs)

    def __init__(self):  # 这里初始化策略参数和指标
        self.log_记录 = []  # 存储日志记录
        bbb = 2
        print('=' * 200)
        print('采用___策略001')
        self.buy_list = []
        total_value = self.broker.getvalue()
        print(f"策略开始时的总资金: {total_value}")
        pass
    def prenext(self):
        self.next()
    def next(self):  # 这里编写策略的逻辑，每个新的市场数据到达时调用一次
        print('-' * 200)
        print( self.datetime.date(0) )
        持仓列表 = [abc._name for abc in self.broker.positions if self.broker.getposition(abc).size > 0]
        print('当前持仓列表', 持仓列表)
        print('当天 目标股票收盘价:',self.getdatabyname('600519').close[0]     )
        # 先卖
        for name_i in  持仓列表:
            print( '股票 :'+str(name_i)+ ' 持仓股数 :'+str(self.getpositionbyname(name_i ).size))
            if self.getpositionbyname(name_i).size >= 0 :
                self.close(name_i)
                pass
        # 后买
        # if self.datetime.date(0).year < 2024:
        #     self.buy('600519', size=100  )
        #     for name_i in 持仓列表:
        #         print('股票 :' + str(name_i) + ' 持仓股数 :' + str(self.getpositionbyname(name_i).size))
        #         if self.getpositionbyname(name_i).size >= 1:
        #             self.close(name_i)
        global bbb
        if bbb >= 1 :
            self.buy('600519', size=100)
            bbb = bbb -1





        print('钱+股票' ,self.broker.getvalue()  )
        print('股票',self.broker.getvalue()-self.broker.getcash() )
        print( '钱',self.broker.getcash() )



        print(' --- 当天已完成交易如下 ---')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:  # 因为我开启cheat 模式 ,直接购买成功了
            pass

        if order.status in [order.Completed]:   # completed  订单已完成
            if order.isbuy():
                print('买入:',order.data._name,'订单', order.ref , end=' ')
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '手续费:', format(order.executed.comm,'.2f') )
            elif order.issell():
                print('卖出:', order.data._name ,'订单', order.ref , end=' ' )
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '手续费:', format(order.executed.comm,'.2f') )

        elif order.status in [order.Canceled]:
            # 订单已取消
            print('订单已取消')
        elif order.status in [order.Rejected]:
            # 订单被拒绝
            print('订单被拒绝')
        elif order.status in [order.Margin]:
            # 订单因保证金问题被取消
            print('因为钱不够,订单已取消')
    def notify_trade(self, trade):   # 对于单只股票,首次买入触发,或则完全卖出的时候触发
        if trade.justopened: # 对于单只股票,0仓位买入时候
            # 交易刚开启
            pass
            # print('--- 触发 开仓 ---')
            # print('买入: ','订单',trade.ref ,'股票',trade.data._name,'开仓价格:', format(trade.price,'.2f'),'开仓数量:', trade.size  ,'持股天数:', trade.barlen ,'毛利润:',  format(trade.pnl,'.2f'), '净利润:', format(trade.pnlcomm,'.2f')  )
        elif trade.isclosed: # 平仓
            print('--- 触发 平仓 ---')
            print('平仓: ',
                '日期',self.datetime.date(-1),
                '订单编号',trade.ref ,
                '股票',trade.data._name,
                '卖出股数',self.getpositionbyname(trade.data._name).size,
                '持仓成本:', format(trade.price,'.2f'),
                '当天卖出价格',self.getdatabyname(trade.data._name).close[-1]- 0.01,
                '涨幅',format(((self.getdatabyname(trade.data._name).close[-1]- 0.01-trade.price)/trade.price *100) ,'.2f'),
                '持股天数:', trade.barlen  ,
                '毛利润:', format(trade.pnl,'.2f'),
                '净利润:', format(trade.pnlcomm,'.2f')  )
            self.log(平仓='平仓',
                    日期=self.datetime.date(-1),
                    订单编号=trade.ref,
                    股票=trade.data._name,
                    卖出股数 = self.getpositionbyname(trade.data._name).size ,
                    持仓成本=trade.price,
                    当天卖出价格=self.getdatabyname(trade.data._name).close[-1]- 0.01 ,
                    涨幅=   (self.getdatabyname(trade.data._name).close[-1]- 0.01-  trade.price)/trade.price *100        ,
                    持股天数=trade.barlen,
                    毛利润=trade.pnl,
                    净利润=trade.pnlcomm,
                    )
        elif trade.isopen:
            # 交易仍然开着（未平仓）
            print('交易仍然开着')
            print('当前未平仓部分的利润:', trade.pnl)
            print('当前价格:', trade.price)
            print('当前数量:', trade.size)
    def notify_cashvalue(self, cash, value):
        pass
        # 打印当前的现金和账户总值
        print('-'*20)
        print(f"当天收盘_现金: {cash:.2f}, 账户总值: {value:.2f}", end=' ')
        print('利润',format(value-初始本金,'.2f')  )
    def stop(self):
        # 策略运行结束时调用
        total_value = self.broker.getvalue()
        print(f"策略结束时的总资金: \n{total_value}")
        pass

class 策略002(bt.Strategy):
    def log(self, **kwargs):
        self.log_记录.append(kwargs)
    def __init__(self):  # 这里初始化策略参数和指标
        self.log_记录 = []  # 存储日志记录
        global lk_账户
        lk_账户 = defaultdict(dict)

        print('=' * 200)
        print('采用___策略001')
        total_value = self.broker.getvalue()
        print(f"策略开始时的总资金: {total_value}")
        pass
    def prenext(self):
        self.next()
    def next(self):  # 这里编写策略的逻辑，每个新的市场数据到达时调用一次
        print('=' * 200)
        next当前日期 = self.datetime.datetime(0)
        print(self.datetime.date(0))
        持仓列表 = [abc._name for abc in self.broker.positions if self.broker.getposition(abc).size > 0]
        当天卖出清单 = []
        # 检查是不是最后一天
        # for data in self.datas:
        #     # 判断当前bar是否是数据集中的最后一个bar
        #     if len(data) == data.buflen()-10:
        #         for i in 持仓列表:
        #             self.close(i)
        #         continue


        print('开盘前_持仓列表', 持仓列表)
        #-------- 先卖#################################################################################################
        for i in 持仓列表 :
            持仓成本 = self.getpositionbyname( i ).price
            现在价格 = self.getpositionbyname( i ).adjbase
            股数 = self.getpositionbyname( i ).size
            持仓天数 = len(self.getdatabyname(i)) - lk_账户[i]['开仓_bar'] + 1
            print(i ,'持仓成本:',小数2点(持仓成本) ,'现在价格:',小数2点(现在价格) ,'股数:',股数 , '持仓天数:',持仓天数 )
            if  self.getpositionbyname( i ).price*0.95 > self.getpositionbyname( i ).adjbase :
                self.close(i)
                当天卖出清单.append(i)
            if  self.getpositionbyname( i ).price*1.05 < self.getpositionbyname( i ).adjbase :
                self.close(i)
                当天卖出清单.append(i)



        #-------- 后买####################################################################################################

        # 检查该日期是否在排序买入清单中
        if next当前日期 in 排序买入清单       :
            # 获取当前日期的买入清单,减去卖出清单,别当天卖,当天买,这个傻逼行为
            当天买入清单 = set(排序买入清单[next当前日期]) - set(当天卖出清单)

        else:
            print(f"{next当前日期} : 没有买入清单")
        for i in 当天买入清单 :
            self.buy(i, size=100)
            print( i , self.getdatabyname(i).close[0])







        print('钱+股票' ,self.broker.getvalue()  )
        print('股票',self.broker.getvalue()-self.broker.getcash() )
        print( '钱',self.broker.getcash() )

        print(' --- 当天已完成交易如下 ---')
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:  # 因为我开启cheat 模式 ,直接购买成功了
            pass
        if order.status in [order.Completed]:   # completed  订单已完成
            if order.isbuy():
                lk_账户[order.data._name]['合计size'] =lk_账户[order.data._name].get('合计size', 0) +order.executed.size
                print('买入:',order.data._name,'订单', order.ref , end=' ')
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '买入价格',小数2点(order.executed.price),
                '手续费:', 小数2点(order.executed.comm ),
                )
            elif order.issell():
                print('卖出:', order.data._name ,'订单', order.ref , end=' ' )
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '卖出价格', 小数2点(order.executed.price),
                '手续费:', 小数2点(order.executed.comm ),
                )
        elif order.status in [order.Canceled]:
            # 订单已取消
            print('订单已取消')
        elif order.status in [order.Rejected]:
            # 订单被拒绝
            print('订单被拒绝')
        elif order.status in [order.Margin]:
            # 订单因保证金问题被取消
            print('因为钱不够,订单已取消')
    def notify_trade(self, trade):   # 对于单只股票,首次买入触发,或则完全卖出的时候触发
        if trade.justopened: # 对于单只股票,0仓位买入时候
            print('--- 触发 开仓 ---')
            # print('买入: ','订单',trade.ref ,'股票',trade.data._name,'开仓价格:', format(trade.price,'.2f'),'开仓数量:', trade.size  ,'持股天数:', trade.barlen ,'毛利润:',  format(trade.pnl,'.2f'), '净利润:', format(trade.pnlcomm,'.2f')  )
            lk_账户[trade.data._name]['开仓_bar'] =  len(self.getdatabyname(trade.data._name))
            pass
        elif trade.isclosed: # 平仓

            print('--- 触发 平仓 ---')
            print('平仓: ',
                '日期',self.datetime.date(-1),
                '订单编号',trade.ref ,
                '股票',trade.data._name,
                '卖出股数',lk_账户[trade.data._name]['合计size'],
                '持仓成本:', 小数2点(trade.price),
                '当天卖出价格',小数2点(self.getdatabyname(trade.data._name).close[-1]- 0.01),
                '涨幅',小数2点 ((self.getdatabyname(trade.data._name).close[-1]- 0.01-trade.price)/trade.price *100)  ,
                '持股天数:', trade.barlen  ,
                '毛利润:', 小数2点(trade.pnl),
                '净利润:', 小数2点(trade.pnlcomm)
                )
            del lk_账户[trade.data._name]
            self.log(平仓='平仓',
                    日期=self.datetime.date(-1),
                    订单编号=trade.ref,
                    股票=trade.data._name,
                    卖出股数 = self.getpositionbyname(trade.data._name).size ,
                    持仓成本=trade.price,
                    当天卖出价格=self.getdatabyname(trade.data._name).close[-1]- 0.01 ,
                    涨幅=   (self.getdatabyname(trade.data._name).close[-1]- 0.01-  trade.price)/trade.price *100        ,
                    持股天数=trade.barlen,
                    毛利润=trade.pnl,
                    净利润=trade.pnlcomm,
                    )
        elif trade.isopen:
            # 交易仍然开着（未平仓）
            print('交易仍然开着')
            print('当前未平仓部分的利润:', trade.pnl)
            print('当前价格:', trade.price)
            print('当前数量:', trade.size)
    def notify_cashvalue(self, cash, value):
        pass
        # # 打印当前的现金和账户总值
        # print('-'*20)
        # print('当天收盘_现金: ',小数2点(cash), '账户总值: ', 小数2点(value), end=' ')
        # print('利润',小数2点(value-初始本金)   )
    def stop(self):
        # 策略运行结束时调用
        total_value = self.broker.getvalue()
        print(f"策略结束时的总资金: \n{total_value}")
        pass

class 策略003(bt.Strategy):
    def log(self, **kwargs):
        self.log_记录.append(kwargs)
    def __init__(self):  # 这里初始化策略参数和指标
        self.log_记录 = []  # 存储日志记录
        global lk_账户
        lk_账户 = defaultdict(dict)
        lk_账户['现金']= 初始本金

        print('=' * 200)
        print('采用___策略001')
        total_value = self.broker.getvalue()
        print(f"策略开始时的总资金: {total_value}")
        pass
    def prenext(self):
        self.next()
    def next(self):  # 这里编写策略的逻辑，每个新的市场数据到达时调用一次
        print('=' * 200)
        next当前日期 = self.datetime.datetime(0)
        print(self.datetime.date(0))
        持仓列表 = [abc._name for abc in self.broker.positions if self.broker.getposition(abc).size > 0]
        当天卖出清单 = []
        # 检查是不是最后一天
        for data in self.datas:
            # 判断当前bar是否是数据集中的最后一个bar
            if len(data) > data.buflen()-2:
                for i in 持仓列表:
                    self.close(i)
            else :
                print('开盘前_持仓列表', 持仓列表)
                #-------- 先卖#################################################################################################
                for i in 持仓列表 :
                    持仓成本 = self.getpositionbyname( i ).price
                    现在价格 = self.getpositionbyname( i ).adjbase
                    股数 = self.getpositionbyname( i ).size
                    持仓天数 = len(self.getdatabyname(i)) - lk_账户[i]['开仓_bar'] + 1
                    print(i ,'持仓成本:',小数2点(持仓成本) ,'现在价格:',小数2点(现在价格) ,'股数:',股数 , '持仓天数:',持仓天数 )
                    if  self.getpositionbyname( i ).price*0.95 > self.getpositionbyname( i ).adjbase :
                        self.close(i)
                        当天卖出清单.append(i)
                    if  self.getpositionbyname( i ).price*1.05 < self.getpositionbyname( i ).adjbase :
                        self.close(i)
                        当天卖出清单.append(i)



                #-------- 后买####################################################################################################

                # 检查该日期是否在排序买入清单中
                if next当前日期 in 排序买入清单       :
                    # 获取当前日期的买入清单,减去卖出清单,别当天卖,当天买,这个傻逼行为
                    当天买入清单 = set(排序买入清单[next当前日期]) - set(当天卖出清单)

                else:
                    print(f"{next当前日期} : 没有买入清单")
                for i in 当天买入清单 :
                    self.buy(i, size=100)
                    print( i , self.getdatabyname(i).close[0])






        print( '钱',小数2点(self.broker.getcash()) ,end=' ')
        print('股票',小数2点(self.broker.getvalue()-self.broker.getcash()) ,end=' ' )
        print('钱+股票' ,小数2点(self.broker.getvalue()) ,end=' ' )
        print('盈利',小数2点(self.broker.getvalue()- 初始本金 ))

        print(' --- 当天已完成交易如下 ---')
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:  # 因为我开启cheat 模式 ,直接购买成功了
            pass
        if order.status in [order.Completed]:   # completed  订单已完成
            if order.isbuy():
                lk_账户[order.data._name]['合计size'] =lk_账户[order.data._name].get('合计size', 0) +order.executed.size
                lk_账户['现金']=lk_账户['现金']+(-order.executed.size*order.executed.price-order.executed.comm)
                print('买入:',order.data._name,'订单', order.ref , end=' ')
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '买入价格',小数2点(order.executed.price),
                '手续费:', 小数2点(order.executed.comm ),
                '现金变动', 小数2点(-order.executed.size*order.executed.price-order.executed.comm),
                '现金余额',小数2点(lk_账户['现金']),
                )

            elif order.issell():
                lk_账户['现金']=lk_账户['现金']+(-order.executed.size*order.executed.price-order.executed.comm)
                print('卖出:', order.data._name ,'订单', order.ref , end=' ' )
                print('日期:', self.data.num2date(order.executed.dt).date(),
                '数量:', order.executed.size,
                '卖出价格', 小数2点(order.executed.price),
                '手续费:', 小数2点(order.executed.comm ),
                '现金变动', 小数2点(order.executed.size*order.executed.price-order.executed.comm),
                '现金余额',小数2点(lk_账户['现金']),
                )
        elif order.status in [order.Canceled]:
            # 订单已取消
            print('订单已取消')
        elif order.status in [order.Rejected]:
            # 订单被拒绝
            print('订单被拒绝')
        elif order.status in [order.Margin]:
            # 订单因保证金问题被取消
            print('因为钱不够,订单已取消')
    def notify_trade(self, trade):   # 对于单只股票,首次买入触发,或则完全卖出的时候触发
        if trade.justopened: # 对于单只股票,0仓位买入时候
            print('--- 触发 开仓 ---')
            # print('买入: ','订单',trade.ref ,'股票',trade.data._name,'开仓价格:', format(trade.price,'.2f'),'开仓数量:', trade.size  ,'持股天数:', trade.barlen ,'毛利润:',  format(trade.pnl,'.2f'), '净利润:', format(trade.pnlcomm,'.2f')  )
            lk_账户[trade.data._name]['开仓_bar'] =  len(self.getdatabyname(trade.data._name))
            pass
        elif trade.isclosed: # 平仓

            print('--- 触发 平仓 ---')
            print('平仓: ',
                '日期',self.datetime.date(-1),
                '订单编号',trade.ref ,
                '股票',trade.data._name,
                '卖出股数',lk_账户[trade.data._name]['合计size'],
                '持仓成本:', 小数2点(trade.price),
                '当天卖出价格',小数2点(self.getdatabyname(trade.data._name).close[-1]- 0.01),
                '涨幅',小数2点 ((self.getdatabyname(trade.data._name).close[-1]- 0.01-trade.price)/trade.price *100)  ,
                '持股天数:', trade.barlen  ,
                '毛利润:', 小数2点(trade.pnl),
                '净利润:', 小数2点(trade.pnlcomm)
                )
            del lk_账户[trade.data._name]
            self.log(平仓='平仓',
                    日期=self.datetime.date(-1),
                    订单编号=trade.ref,
                    股票=trade.data._name,
                    卖出股数 = self.getpositionbyname(trade.data._name).size ,
                    持仓成本=trade.price,
                    当天卖出价格=self.getdatabyname(trade.data._name).close[-1]- 0.01 ,
                    涨幅=   (self.getdatabyname(trade.data._name).close[-1]- 0.01-  trade.price)/trade.price *100        ,
                    持股天数=trade.barlen,
                    毛利润=trade.pnl,
                    净利润=trade.pnlcomm,
                    )
        elif trade.isopen:
            # 交易仍然开着（未平仓）
            print('交易仍然开着')
            print('当前未平仓部分的利润:', trade.pnl)
            print('当前价格:', trade.price)
            print('当前数量:', trade.size)
    def notify_cashvalue(self, cash, value):
        pass
        # # 打印当前的现金和账户总值
        # print('-'*20)
        # print('当天收盘_现金: ',小数2点(cash), '账户总值: ', 小数2点(value), end=' ')
        # print('利润',小数2点(value-初始本金)   )
    def stop(self):
        # 策略运行结束时调用
        total_value = self.broker.getvalue()
        print( '策略结束时的总资金: ',小数2点(total_value))
        pass


策略列表 = []
策略列表.append( 策略000 )
策略列表.append( 策略001 )
策略列表.append( 策略002 )
策略列表.append( 策略003 )
















# todo 主程序设置 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

cerebro = bt.Cerebro(
    cheat_on_open=True ,    # 开启作弊模式
    # stdstats=False       # 默认是True,观察器选择False,能提升速度,观察器的打开,记录数据只会显示在官方的plt图上,用不上
    )
cerebro.broker.set_coc(True)  # 设置 能以当日收盘价成交
# 调用投喂函数,开始投喂df
if not os.path.exists('回测缓存文件.pkl'):
    print('不存在_回测缓存文件________开始加载')
    df.groupby('代码').apply(lambda df: feed投喂(df, cerebro), include_groups=False)
else:
    print('存在_回测缓存文件_______开始欺骗餐')
    df测试 = 欺骗餐()
    data测试 = bt.feeds.PandasData(dataname=df测试)
    cerebro.adddata( data测试 )

# 设置初始资金
cerebro.broker.setcash(初始本金)
# 设置手续费比例
cerebro.broker.setcommission(commission=0.002)
# 设置双边滑点
cerebro.broker.set_slippage_fixed(fixed=0.01)  #固定0.01滑点
# 添加策略
cerebro.addstrategy( 策略列表[采用策略的序号] )

# 运行回测
if not os.path.exists('回测缓存文件.pkl'):
    results = cerebro.run(save_my_data=True)  #运行程序,保存数据
else :
    results = cerebro.run(load_my_data=True)  # 运行程序,加载数据

strat = results[0]
log_记录 = strat.log_记录
平仓记录_df = pd.DataFrame(log_记录)
print(平仓记录_df  )
if len( 平仓记录_df) :

    赚钱次数1 =  len(平仓记录_df[平仓记录_df['净利润'] > 0])
    胜率 =    赚钱次数1/ len(平仓记录_df )
    净利润 =  平仓记录_df['净利润'].sum()
    print('赚'*100)
    print('策略结果:')
    print('胜率:', 小数2点(胜率),'净利润:',小数2点(净利润))
    print('初始本金',初始本金 ,'最终本金',小数2点(cerebro.broker.getvalue()),
            '净利润:',小数2点(cerebro.broker.getvalue()-初始本金) )



结束时间 = time.time()
运行时间 = 结束时间 - 开始时间
print("运行时间：", 小数2点(运行时间), "秒")

# cerebro.plot()



















