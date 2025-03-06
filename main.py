import ccxt
import pandas as pd

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
    dframe = pd.DataFrame(candles, columns=['timestamp', 'open', 'high',
                                            'low', 'close', 'volume'])
    return dframe

# Trading Strategy
def trading_strategy(dframe):
    '''Generate BUY/SELL signal using SMA strategy'''

    dframe['SMA_5'] = dframe['close'].rolling(window=5).mean()
    dframe['SMA_20'] = dframe['close'].rolling(window=20).mean()

    # SMA_5 cross above SMA_20 - BUY Signal
    if (dframe['SMA_5'].iloc[-1] > dframe['SMA_20'].iloc[-1] 
        and dframe['SMA_5'].iloc[-2] <= dframe['SMA_20'].iloc[-2]):
        return 'BUY'
    
    # SMA_5 cross below SMA_20 - SELL Signal
    elif (dframe['SMA_5'].iloc[-1] < dframe['SMA_20'].iloc[-1] 
        and dframe['SMA_5'].iloc[-2] >= dframe['SMA_20'].iloc[-2]):
        return 'SELL'

    # Neither - HOLD Signal
    else:
        return 'HOLD'
    
dframe = fetch_data(tpair)
tsignal = trading_strategy(dframe)

print(dframe) # Checks data fetch is working
print(tsignal) # Checks trading strategy is working