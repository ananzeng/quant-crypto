import requests
import numpy as np
from sklearn.linear_model import LinearRegression

def get_historical_data(symbol, interval, limit):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(data)
    #for index, item in enumerate(data):
    #    print(index, item[4])

    return [float(item[4]) for item in data]  # 取收盤價

def calculate_returns(prices):
    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]
    return returns

def calculate_beta(crypto_returns, btc_returns):
    X = np.array(btc_returns).reshape(-1, 1)
    y = np.array(crypto_returns)
    model = LinearRegression().fit(X, y)
    return model.coef_[0]

def standardize_returns(crypto_returns, beta):
    return [ret / beta for ret in crypto_returns]

def calculate_betas_and_standardized_returns(symbols, interval='1d', limit=10):
    btc_prices = get_historical_data('BTCUSDT', interval, limit)
    btc_returns = calculate_returns(btc_prices)
    
    crypto_prices = {symbols: get_historical_data(symbols, interval, limit)}
    crypto_returns = {symbol: calculate_returns(prices) for symbol, prices in crypto_prices.items()}
    
    betas = {symbols: calculate_beta(crypto_returns[symbols], btc_returns)}
    standardized_returns = {symbols: standardize_returns(crypto_returns[symbols], betas[symbols])}
    
    return betas, standardized_returns

if __name__ == "__main__":
    # 示例输入参数
    symbols = 'ETHUSDT'  # 用户可以自定义输入symbol列表
    interval = '1d'
    limit = 10
    
    betas, standardized_returns = calculate_betas_and_standardized_returns(symbols, interval, limit)
    
    # 输出结果
    print("Betas:", betas)
    print("Standardized Returns:", standardized_returns)
