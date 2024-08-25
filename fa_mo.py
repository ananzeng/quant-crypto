import pandas as pd
import requests
from datetime import datetime, timedelta

# Binance API 基本 URL
BASE_URL = 'https://api.binance.com'

# 獲取加密貨幣歷史數據
def get_historical_data(symbol, start_date, end_date, interval='1d'):
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(start_date.timestamp() * 1000),  # 轉換為毫秒
        'endTime': int(end_date.timestamp() * 1000),      # 轉換為毫秒
        'limit': 1000  # 默認返回1000條數據
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])
    return df[['close', 'volume']]

# 計算每日回報率
def calculate_daily_return(df):
    df['Daily Return'] = df['close'].pct_change()
    return df

# 計算三週動能
def calculate_momentum(df, weeks=3):
    df['Cumulative Return'] = df['Daily Return'].rolling(window=weeks * 7).sum()  # 7天一週
    df['Momentum'] = df['Cumulative Return'].shift(1)  # 延遲一週
    return df

# 設置起始和結束日期
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * 2)  # 過去兩年的數據

# 定義要分析的加密貨幣
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']

# 下載數據並計算動能
momentum_data = {}
for symbol in symbols:
    symbol_data = get_historical_data(symbol, start_date, end_date)
    symbol_data = calculate_daily_return(symbol_data)
    symbol_data = calculate_momentum(symbol_data)
    momentum_data[symbol] = symbol_data

# 輸出每個加密貨幣的動能
for symbol, df in momentum_data.items():
    print(f'\n{symbol} Momentum:\n', df[['Momentum']].dropna().tail())

# 假設一個簡單的策略：買入動能最高的加密貨幣，賣空動能最低的加密貨幣
momentum_scores = {symbol: df['Momentum'].iloc[-1] for symbol, df in momentum_data.items()}
sorted_momentum = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)

# 輸出策略建議
print("\nStrategy Recommendation:")
print("Long the highest momentum cryptocurrencies and Short the lowest momentum cryptocurrencies.")
for symbol, momentum in sorted_momentum:
    print(f'{symbol}: Momentum = {momentum:.2f}')
