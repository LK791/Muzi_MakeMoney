


import backtrader as bt

# 创建策略类
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 添加移动平均线指标
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=20)

    def next(self):
        # 如果收盘价大于移动平均线的值，则买入
        if self.data.close[0] > self.sma[0]:
            self.buy()

        # 如果收盘价小于移动平均线的值，则卖出
        if self.data.close[0] < self.sma[0]:
            self.sell()

# 创建 Cerebro 引擎实例
cerebro = bt.Cerebro()

# 加载数据
data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2010, 1, 1), todate=datetime(2020, 12, 31))

# 将数据添加到 Cerebro 引擎
cerebro.adddata(data)

# 将策略添加到 Cerebro 引擎
cerebro.addstrategy(MyStrategy)

# 设置初始资金
cerebro.broker.setcash(100000.0)

# 设置每次交易的股票数量
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# 运行回测
cerebro.run()

# 打印最终资金
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
