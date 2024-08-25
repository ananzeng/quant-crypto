import pandas as pd
import requests
import ta


# 定義函數來獲取K線數據
def get_historical_klines(symbol, interval, start_str = None, end_str=None):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_str,
        "endTime": end_str,
        "limit": 1000
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    #print(data)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['close'].astype(float)
    
    return df


# 獲取所有現貨交易對
def cal_vegas(symbol, interval_list):
    results = []
    
    if len(interval_list) == 1:
        interval_list = [interval_list]


    # 獲取BTC-USD的日線數據
    for interval in interval_list:
        btc_data = get_historical_klines(symbol, interval)
        #print(btc_data["close_time"])
        # 計算EMA
        btc_data['EMA12'] = ta.trend.ema_indicator(btc_data['close'], window=12)
        btc_data['EMA144'] = ta.trend.ema_indicator(btc_data['close'], window=144)
        btc_data['EMA169'] = ta.trend.ema_indicator(btc_data['close'], window=169)
        btc_data['EMA576'] = ta.trend.ema_indicator(btc_data['close'], window=576)
        btc_data['EMA676'] = ta.trend.ema_indicator(btc_data['close'], window=676)

        # 當前價格
        current_price = btc_data['close'].iloc[-1]
        current_ema12 = btc_data['EMA12'].iloc[-1]
        current_ema144 = btc_data['EMA144'].iloc[-1]
        current_ema169 = btc_data['EMA169'].iloc[-1]
        current_ema576 = btc_data['EMA576'].iloc[-1]
        current_ema676 = btc_data['EMA676'].iloc[-1]


        # 檢查看多條件
        bullish = (current_price > current_ema144 and current_price > current_ema169 and
                current_ema12 > current_ema144 and current_ema12 > current_ema169 and
                current_price > current_ema576 and current_price > current_ema676)

        results.append(bullish)

    return results
    
if __name__ == "__main__":
    # 示例输入参数
    symbols = 'ETHUSDT'  # 用户可以自定义输入symbol列表
    interval_list = ["1h", "2h", "4h", "12h", "1d"]
    results = cal_vegas(symbols, interval_list)
    
    # 输出结果
    print("results:", results)
