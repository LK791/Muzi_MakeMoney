


import backtrader as bt
import pandas as pd
from datetime import datetime
import time
start_time = time.time()
import matplotlib.pyplot as plt




# 设置输出右对齐
pd.set_option('display.unicode.east_asian_width', True)
# 显示所有的列
pd.set_option('expand_frame_repr', False)
# 最多显示数据的行数
pd.set_option('display.max_rows', 5000)
# 取消科学计数法,显示完整,可调整小数点后显示位数
pd.set_option('display.float_format', '{:.2f}'.format)



cash_value = {}


class Mystrategy(bt.Strategy):
    def __init__(self):
        pass

    def start(self):
        print("start")

    def prenext(self):
        print("prenext")

    def next(self):
        cash_value.update({str(self.datetime.date(0)): self.broker.getvalue()})
        print("next")






df = pd.read_csv("/Users/likai/Desktop/Python股票量化投资课程/00股票量化配套代码/xbx_stock_2019_完整代码/Backtrader/第0轮/601688.csv",
                parse_dates=['time']
                )

df["time"] = pd.to_datetime(df["time"])

data = bt.feeds.PandasData(
    dataname=df,
    fromdate=datetime(2021, 5, 10),
    todate=datetime(2022, 5, 10),
    datetime='time',
    open='open',
    high='high',
    low='low',
    close='close',
    volume='volume',
    openinterest=-1
)
cerebro = bt.Cerebro()
cerebro.adddata(data, name="daily_kline")
cerebro.addstrategy(Mystrategy)
result = cerebro.run()

cerebro.plot()
# cash_value = pd.Series(cash_value)
# cash_value.plot(figsize=(18,6))
plt.show()
