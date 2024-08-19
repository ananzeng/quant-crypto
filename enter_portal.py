import requests
import numpy as np
from beta import calculate_betas_and_standardized_returns
from adx import calculate_adx

# 獲取虛擬貨幣列表
def get_crypto_list():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols'] if symbol['quoteAsset'] == 'USDT']
    return symbols

# 獲取歷史數據
def get_historical_data(symbol, interval='1d', limit=10):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    #print("symbol", symbol)
    #print("data", data)
    return [float(item[4]) for item in data]  # 取收盤價


def main():
    symbols = get_crypto_list()
    interval = '1h'
    limit = 100
    #print("symbols", symbols)
    for symbol in symbols:
        #print(symbol)
        data = get_historical_data(symbol)
        #print(data)
        betas, standardized_returns = calculate_betas_and_standardized_returns(symbol, interval, limit)
        print(betas)
        print(standardized_returns)
        result_df = calculate_adx(symbol, interval, limit, period=14)
        print(result_df)
        break
if __name__ == "__main__":
    main()