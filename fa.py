import requests
import math
from dotenv import load_dotenv
import os

def cal_cap(symbols):
# 加载 .env 文件中的变量
    load_dotenv()

    # 获取 API 密钥
    api_key = os.getenv('COINMARKETCAP_API_KEY')
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # 设置要查询的symbol

    symbol_str = ','.join(symbols)

    # 发送请求获取指定symbol的加密货币市场数据
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': symbol_str,
        'convert': 'USD'
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # 计算市值因子（Size Factor）
    size_factors = []
    for symbol in symbols:
        crypto = data['data'][symbol]
        market_cap = crypto['quote']['USD']['market_cap']
        log_market_cap = math.log(market_cap) if market_cap > 0 else 0  # 计算市值的自然对数
        size_factors.append({
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'market_cap': market_cap,
            'log_market_cap': log_market_cap
        })

    # 打印结果
    for sf in size_factors:
        print(f"Name: {sf['name']}, Symbol: {sf['symbol']}, Market Cap: {sf['market_cap']}, Size Factor: {sf['log_market_cap']}")

    return size_factors
if __name__ == "__main__":
    # 示例输入参数
    symbols = ['BTC', 'ETH', 'XRP'] # 用户可以自定义输入symbol列表
    results = cal_cap(symbols)
    
    # 输出结果
    print("results:", results)