

import sqlite3
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
from MyTT import *
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
pd.set_option('display.max_rows', 5000)
# 取消科学计数法,显示完整,可调整小数点后显示位数
# pd.set_option('display.float_format', '{:.2f}'.format)




##########################################################################
##########################################################################
##########################################################################




# 读取sql,存入hdf

# conn=sqlite3.connect(r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/stock_2018.db')
#
# stock_daily = pd.read_sql("select * from stock_daily     ", con=conn)
# stock_daily.to_hdf(
#     r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
#     key='all_data',
#     mode='w'
# )


# 读取hdf,读取到   df   ,使用 hdf  ,确实速度很快

df = pd.read_hdf(
    r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
    key='all_data',
    parse_dates=['交易日期']
)

# print(df.columns)
# exit()


# 所有股票名 = df['股票简称'].unique()
# for  i  in  所有股票名:
#     print(i)
# print(len(所有股票名 ))

df.columns = ['index', 'date', '股票代码', '股票简称', 'open', 'high',
        'low', 'close', 'volume', '成交额(千元)', '换手率(%)', '量比',
        '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率', '市销率',
        '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)',
        '流通股本(万股)', '总市值(万元)', '流通市值(万元)']

df= df[['date', '股票代码', '股票简称',"open","high","low","close","volume"]]



# print(df)
# end_time = time.time()
# execution_time = end_time - start_time
# print("运行时间：", execution_time, "秒")
# exit()




# 定义处理函数
def zbcl(stock_data):
    C = stock_data['close'].values
    O = stock_data['open'].values
    H = stock_data['high'].values
    L = stock_data['low'].values
    大于ma90天数 = BARSLASTCOUNT(C > MA(C,90) )
    大于ma90天数 = list(np.array(大于ma90天数, dtype=int))
    正能量 =  (C-MA(C,90))/(MA(C,90) )
    stock_data['正能量'] = 正能量
    正能量 = stock_data['正能量'].fillna(0)
    stock_data['psy_1'], stock_data['psy_ma'] = PSY(C, N=12, M=6)
    stock_data['正能量'] = 正能量
    stock_data['大于ma90天数'] = 大于ma90天数
    # aa = stock_data['大于ma90天数'].values
    # stock_data['正能量合集'] = [stock_data['正能量'][(i - aa[i]):(i + 1)].sum() for i in range(len(aa))]
    aa = stock_data['大于ma90天数'].values
    positive_energy = stock_data['正能量'].values
    # 创建一个索引数组，用于提取对应的正能量值
    indices = np.arange(len(aa))
    start_indices = indices - aa+1
    end_indices = indices + 1
    # 使用切片和sum函数进行向量化计算
    result = np.array([positive_energy[start:end].sum() for start, end in zip(start_indices, end_indices)])
    # 将结果赋值给df['正能量合集']
    stock_data['正能量合集'] = result

    return stock_data

# 使用groupby对每个股票进行处理
df = df.groupby('股票代码',group_keys=False).apply(lambda x: zbcl(x))





def buy(df02):
    buy_date = []
    df02['正能排序'] = df02['正能量合集'].rank(ascending=True, pct=True)
    df02['psy排序'] = df02['psy_1'].rank(ascending=False, pct=True)
    df02['因子合集'] = df02['psy排序'] + df02['正能排序']
    df02 = df02.sort_values(by='因子合集', ascending=False)
    buy_date = list(df02['股票代码'].values[:5])
    return  buy_date

aa = df.groupby('date',group_keys=False).apply(lambda x: buy(x))
buy_date = dict(aa)
















