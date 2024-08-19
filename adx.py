import ccxt
import pandas as pd

def calculate_adx(symbol, interval, limit, period):
    symbol = symbol[:-4] + "/USDT"
    #print(symbol)
    # 初始化 Binance 交易所
    exchange = ccxt.binance()
    
    # 獲取歷史數據
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)

    # 將數據轉換為 pandas DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # 計算真實範圍（True Range, TR）
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = (df['high'] - df['close'].shift()).abs()
    df['low_close'] = (df['low'] - df['close'].shift()).abs()
    df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)

    # 計算方向變動（+DM 和 -DM），保持正值
    df['+DM'] = df['high'].diff()
    df['-DM'] = -df['low'].diff()

    df['+DM'] = df.apply(lambda row: row['+DM'] if row['+DM'] > 0 and row['+DM'] > row['-DM'] else 0, axis=1)
    df['-DM'] = df.apply(lambda row: row['-DM'] if row['-DM'] > 0 and row['-DM'] > row['+DM'] else 0, axis=1)

    # 使用指數平滑計算平滑的 TR 和 +DM, -DM
    df['SmoothedTR'] = df['TR'].ewm(span=period, adjust=False).mean()
    df['Smoothed+DM'] = df['+DM'].ewm(span=period, adjust=False).mean()
    df['Smoothed-DM'] = df['-DM'].ewm(span=period, adjust=False).mean()

    # 計算方向指標（+DI 和 -DI）
    df['+DI'] = 100 * (df['Smoothed+DM'] / df['SmoothedTR'])
    df['-DI'] = 100 * (df['Smoothed-DM'] / df['SmoothedTR'])

    # 計算方向性指數（DX）
    df['DX'] = 100 * (df['+DI'] - df['-DI']).abs() / (df['+DI'] + df['-DI'])

    # 計算平均方向性指數（ADX）
    df['ADX'] = df['DX'].rolling(window=period).mean()

    return df[['timestamp', 'ADX', '+DI', '-DI']].dropna()

if __name__ == "__main__":
    # 示例用法
    result_df = calculate_adx(symbol='BTC/USDT', interval='1h', limit=500, period=14)
    print(result_df)
