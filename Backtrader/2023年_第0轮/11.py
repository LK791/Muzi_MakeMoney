
from   insight_python  import common
from   insight_python.insight.query  import *
from   insight_python.market_service  import  market_service



# from insight_python.com.insight import common
# from insight_python.com.insight.query import *
# from insight_python.com.insight.market_service import market_service
from datetime import datetime


def login():
    # 登陆前 初始化
    user = "MDIL1_00160"
    password = "c943r_7.M+59A"
    common.login(market_service, user, password)


login()
df = get_kline(htsc_code=["000001.SZ"], time=[datetime(2021, 5, 10), datetime(2022, 5, 10)],
                   frequency="daily", fq="none")

print(df)