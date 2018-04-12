# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
import tushare as ts
from scipy import  stats
import statsmodels.api as sm
#以上的大部分增强包并没有在函数中使用，而是用于前期的研究过程，参见iPython Notebook文件

def init(context):
    #***context内引入全局变量s1，存储目标合约信息***
    context.s1 = 'CU88'

    #这是可删改的全局变量，也可增加需要的全局变量
    context.OBSERVATION = 200


    #***初始化时订阅合约行情。订阅之后的合约行情会在handle_bar中进行更新***
    subscribe(context.s1)
    #***控制日志输出信号***
    context.first = 1
    #***控制交易信号***
    context.ifbuy = 0


def before_trading(context):
    
    #获取历史收盘价序列，history_bars函数直接返回ndarray，方便之后的有关指标计算，根据需求删改
    #获取的数据进行对数化处理。
    prices = history_bars(context.s1, context.OBSERVATION, '1d', 'close')
    ts_log = np.log(prices)
    #预测价格，策略为今日价格涨跌与昨日相同，根据需求删改
    arima = ARIMA(ts_log,order=(1,1,0))
    results = arima.fit()
    #根据前期研究，最好的ARIMA模型是ARIMA(1,1,0),一阶差分和一阶自回归，没有滑动平均过程
    test_predict = np.exp(results.fittedvalues[-1])
    #模型拟合出的不是实际值，而是变化率，因此接下来输出时还有一点数学计算，但现在还需要把对数处理还原。
    
    #***输出昨日收盘价格和今日预测价格到日志***
    if context.first != 0:
        logger.info('Forecast_price:{}'.format(test_predict * history_bars(context.s1, 1, '1d', 'close')[0]))
        logger.info('Last_day_close:{}'.format(history_bars(context.s1,2,'1d','close')[0]))
        #输出预测值（Forecast_price）和前一交易日收盘价（Last_day_close）
    else:
        context.first = 1
    logger.info('Real_price:{}'.format(history_bars(context.s1, 1, '1d', 'close')[0]))
    #输出当日实际价格

def handle_bar(context, bar_dict):
    # ***进行当天交易***
    '''
    if context.ifbuy == 1:
        #***进行买入开仓操作***
        sell_qty = context.portfolio.positions[context.s1].sell_quantity
        #***先判断当前卖方仓位，如果有，则进行平仓操作***
        if sell_qty > 0:
            buy_close(context.s1, 1)
        #***买入开仓***
        buy_open(context.s1, 1)

    else:
        #***进行卖出开仓操作***
        buy_qty = context.portfolio.positions[context.s1].buy_quantity
        #***先判断当前买方仓位，如果有，则进行平仓操作***
        if buy_qty > 0:
            sell_close(context.s1, 1)
        #***卖出开仓***
        sell_open(context.s1, 1)
    '''
    pass


def after_trading(context):
    # ***输出今日实际价格到日志***
    # prices = history_bars(context.s1, 1, '1d', 'close')
    # ***录入日志***
    # logger.info('Real price:{}'.format(prices[0]))
    pass