import sqlite3
import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime

import matplotlib.pyplot as plt
# import talib


def 获取单个df():
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
    #
    df = pd.read_hdf(
        r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
        key='all_data',
        parse_dates=['交易日期']
    )

    df.columns = ['index', 'time', '股票代码', '股票简称', 'open', 'high',
            'low', 'close', 'volume', '成交额(千元)', '换手率(%)', '量比',
            '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率', '市销率',
            '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)',
            '流通股本(万股)', '总市值(万元)', '流通市值(万元)']
    df= df[['time', '股票代码', '股票简称',"open","high","low","close","volume"]]
    df["openinterest"]=0
    所有股票名 = df['股票代码'].unique()
    df = df[df['股票代码'] == 所有股票名[0]]
    df["time"] = df["time"].astype("str").astype("datetime64")

    return df


def 获取多个df( 个数 = 0 ):
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
    #
    df = pd.read_hdf(
        r'/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/00 数据/h5_stock_2018.h5',
        key='all_data',
        parse_dates=['交易日期']
    )

    df.columns = ['index', 'time', '股票代码', '股票简称', 'open', 'high',
                    'low', 'close', 'volume', '成交额(千元)', '换手率(%)', '量比',
                    '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率', '市销率',
                    '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)',
                    '流通股本(万股)', '总市值(万元)', '流通市值(万元)']
    df = df[['time', '股票代码', '股票简称', "open", "high", "low", "close", "volume"]]
    df["openinterest"] = 0
    所有股票名 = df['股票代码'].unique()
    if 个数 >=1 :
        df = df[df['股票代码'].isin(所有股票名[:个数])]
        df["time"] = df["time"].astype("str").astype("datetime64")
        return df
    df = df[df['股票代码'].isin(所有股票名[:])]
    df["time"] = df["time"].astype("str").astype("datetime64")
    return df



def 指标计算(stock_data):
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
# df = df.groupby('股票代码',group_keys=False).apply(lambda x: 指标计算(x))




def 买点(df02 , n=3  ):
    buy_date = []
    df02['正能排序'] = df02['正能量合集'].rank(ascending=True, pct=True)
    df02['psy排序'] = df02['psy_1'].rank(ascending=False, pct=True)
    df02['因子合集'] = df02['psy排序'] + df02['正能排序']
    df02 = df02.sort_values(by='因子合集', ascending=False)
    buy_date = list(df02['股票代码'].values[:n])
    return  buy_date


# aa = df.groupby('time',group_keys=False).apply(lambda x: 买点(x))
# buy_date = dict(aa)





def to_单股处理(syboml, df ):
    return df[df['股票代码']==syboml][['time',"open","high","low","close","volume","openinterest"]]




def 打印list( 列表 ):
    for i  in 列表 :
        print( i)






def get_持仓过( self , name):
    return  self._trades[self.getdatabyname( name )][0]

def get_开仓时间( self , name):
    ''' 需要传入 data的 名字'''
    self.data.num2date(self._trades[self.getdatabyname(name)][0][-1].dtopen).date()