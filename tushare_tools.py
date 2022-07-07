import tushare as ts
import os
def enter_tushare(tushare_token = ''): 
    '''
    用于进入tushare   return pro权限
    tushare_token: tushare获取token密钥，用于获得tushare数据。可在调用的过程中直接填入，也可丢入全局变量。
    优先度: 参数 > path > input
    '''
    try:
        # 尝试调用直接导入的token
        pro = ts.pro_api(tushare_token)
        # 用于测试api的有效性
        pro.trade_cal(exchange='', start_date='20180901', end_date='20180902', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
        print("tushare pro权限GET")
        return pro
    except:
        try:
            # 为了进一步保护token，可选择将token存在电脑的变量中
            envX = os.environ
            tushare_token = envX['TUSHARE_TOKEN']       # 在全局变量中给键命名为TUSHARE_TOKEN，并在值中填入token
            pro = ts.pro_api(tushare_token)
            pro.trade_cal(exchange='', start_date='20180901', end_date='20180902', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
            print("token获得成功")
            return pro
        except:
            try:
                # 亦可手动填入
                tushare_token = input("请输入你的密钥")
                pro = ts.pro_api(tushare_token)
                # 用于测试api的有效性
                pro.trade_cal(exchange='', start_date='20180901', end_date='20180902', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
                print("成功获取tushare pro权限")
                return pro
            except:
                print("获取tushare pro权限失败")
                return None