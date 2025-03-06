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

dframe = fetch_data(tpair)
print(dframe)