import ccxt
import pandas as pd
import time

from config import API_KEY, API_SECRET # Load API Key

# Intialising Binance API - Key needs to be added
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {'defaultType': 'spot'}
})

exchange.set_sandbox_mode(True) # Use when testing with a TestNet API key

tpair = 'BTC/USDT' # Trading pair
tframe = '1m' # Timeframe for price data (1-minute candles)

# Fetch OHCLV (Open-High-Low-Close-Volume) Data
def fetch_data(tpair, tframe="1m", limit=100):
    candles = exchange.fetch_ohlcv(tpair, tframe, limit=limit)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high',
                                            'low', 'close', 'volume'])
    return df

# Trading Strategy
def trading_strategy(df):
    '''Generate BUY/SELL signal using SMA strategy'''

    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_20'] = df['close'].rolling(window=20).mean()

    # SMA_5 cross above SMA_20 - BUY Signal
    if (df['SMA_5'].iloc[-1] > df['SMA_20'].iloc[-1] 
        and df['SMA_5'].iloc[-2] <= df['SMA_20'].iloc[-2]):
        return 'BUY'
    
    # SMA_5 cross below SMA_20 - SELL Signal
    elif (df['SMA_5'].iloc[-1] < df['SMA_20'].iloc[-1] 
        and df['SMA_5'].iloc[-2] >= df['SMA_20'].iloc[-2]):
        return 'SELL'

    # Neither - HOLD Signal
    else:
        return 'HOLD'

# Execute BUY/SELL Orders
def place_order(signal, amount, tpair):
    if signal == 'BUY':
        order = exchange.create_order(tpair, 'market', 'buy', amount)
        print(f"BUY - Placed BUY order for {amount} {tpair}")
        print(order)
    elif signal == 'SELL':
        order = exchange.create_order(tpair, 'market', 'buy', amount)
        print(f"SELL - Placed SELL order for {amount} {tpair}")
        print(order)
    else:
        print("HOLD - No Trade executed")

while True:
    df = fetch_data(tpair)
    signal = trading_strategy(df)
    place_order(signal, 0.01, tpair)

    time.sleep(60)

    #print(df) # Checks data fetch is working
    #print(signal) # Checks trading strategy is working