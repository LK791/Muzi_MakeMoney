

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
# stock_daily = pd.read_sql("select * from stock_daily where 股票代码>'006000.SZ'    ", con=conn)
# stock_daily.to_hdf(
#     r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
#     key='all_data',
#     mode='w'
# )


# 读取hdf,读取到   df   ,使用 hdf  ,确实速度很快

# df = pd.read_hdf(
#     r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
#     key='all_data',
#     parse_dates=['交易日期']
# )

# print(df)


df = pd.read_csv("all_stock_daily_kline_long.csv", index_col=0,parse_dates=['time'])
df["openinterest"]=0
所有股票名 = df['htsc_code'].unique()
df = df[df['htsc_code'].isin(所有股票名[:])]

# 使用 groupby 试试
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
    # 正能量_1 = [ 正能量.rolling(i).sum() for i in 大于ma90天数 ]
    stock_data['psy_1'], stock_data['psy_ma'] = PSY(C, N=12, M=6)
    stock_data['正能量'] = 正能量
    # stock_data['正能量_1'] = 正能量_1
    stock_data['大于ma90天数'] = 大于ma90天数
    # stock_data['大于ma90天数']=stock_data['大于ma90天数']
    return stock_data

# 使用groupby对每个股票进行处理
df = df.groupby('htsc_code',group_keys=False).apply(lambda x: zbcl(x))



#
# aa = df['大于ma90天数'].values
# df['正能量合集'] = [df['正能量'][(i-aa[i]):(i+1)].sum() for i in range(len(aa)) ]

#
aa = df['大于ma90天数'].values
positive_energy = df['正能量'].values

# 创建一个索引数组，用于提取对应的正能量值
indices = np.arange(len(aa))
start_indices = indices - aa
end_indices = indices + 1

# 使用切片和sum函数进行向量化计算
result = np.array([positive_energy[start:end].sum() for start, end in zip(start_indices, end_indices)])

# 将结果赋值给df['正能量合集']
df['正能量合集'] = result

aa = df['大于ma90天数'].values
positive_energy = df['正能量'].values
df['正能量合集'] = df.apply(lambda row: positive_energy[row.name - row['大于ma90天数']:row.name + 1].sum(), axis=1)


print(df)
print()
end_time = time.time()
execution_time = end_time - start_time
print("运行时间：", execution_time, "秒")
exit()









