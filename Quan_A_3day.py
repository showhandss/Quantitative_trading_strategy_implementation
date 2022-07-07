# 不知道为什么不能显示出结果
from logging import exception
import pandas as pd
import tushare as ts
# 用于获取tushare
from tushare_tools import enter_tushare

pro = enter_tushare()
trade_date = pro.trade_cal(start_date=20220101, end_date=20220201, is_open=1)   # 交易款项
amount = {}             # 总资产
currency_amount = {}    # 货币资产
trade_data = pd.DataFrame(columns=['ts_code', 'buy_date', 'buy_price', 'buy_num', 'hold_days', 'sale_date', 'sale_price'])
pre_date = trade_date.loc[0, 'cal_date']
amount[pre_date] = currency_amount[pre_date] = 1000000
for current_date in trade_date.loc[1:, 'cal_date']:
    trade_index = ((trade_data['hold_days']==3) & (trade_data['sale_price']==0))
    sale_num = sale_price = orignal_buy_price = 0
    if len(trade_index) and max(trade_index):
        ts_code = list(trade_data.loc[trade_index, 'ts_code'])[0]
        sale_num = list(trade_data.loc[trade_index, 'buy_num'])[0]
        orignal_buy_price = list(trade_data.loc[trade_index, 'buy_price'])[0]
        sale_price = pro.daily(trade_date = current_date, ts_code = ts_code).loc[0, 'close']
        trade_data.loc[trade_index, ['sale_date', 'sale_price']] = [current_date, sale_price]
    trade_data.loc[trade_data['hold_days']<3, 'hold_days'] += 1
    pre_daily = pro.daily(trade_date = pre_date, fields='ts_code, amount')
    ts_code = pre_daily[pre_daily['amount']==pre_daily.amount.max()].iloc[0, 0]
    buy_price = pro.daily(trade_date = current_date, ts_code = ts_code).iloc[0, 2]
    buy_amount_limit = min(amount[pre_date] / 4, currency_amount[pre_date])
    buy_num = buy_amount_limit // (buy_price * 100)
    print("{}买入{} {}股，买价{}".format(current_date, ts_code, buy_num * 100, buy_price))
    trade_data.loc[len(trade_data),['ts_code', 'buy_date', 'buy_price', 'buy_num', 'hold_days', 'sale_price']] = [ts_code, current_date, buy_price, buy_num, 0, 0]
    currency_amount[current_date] = currency_amount[pre_date] - buy_price * buy_num * 100 + sale_num * sale_price * 100
    amount[current_date] = amount[pre_date] + (sale_price - orignal_buy_price) * sale_num * 100
    pre_date = current_date
print(trade_data)
print(amount)