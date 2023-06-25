from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import os 

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")
class CryptoTrade:
    def __init__(self, symbol, interval, limit):
        client = Client(api_key, api_secret)
        self.candles = client.get_klines(symbol, interval, limit) 

    # candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1WEEK, limit=15)
    def dataframe_creation(self):
        timestamps = [candle[0] for candle in self.candles]
        opens = [float(candle[1]) for candle in self.candles]
        highs = [float(candle[2]) for candle in self.candles]
        lows = [float(candle[3]) for candle in self.candles]
        closes = [float(candle[4]) for candle in self.candles]
        volumes = [float(candle[5]) for candle in self.candles]

        self.dataframe = pd.DataFrame({
            'Timestamp': timestamps,
            'Open': opens,
            'High': highs,
            'Low': lows,
            'Close': closes,
            'Volume': volumes
        })
 
    def bullish_crossover(self, short_period, long_period):
        closes = self.dataframe['Close'].tolist()
        # print(closes)
        # short_period = 7
        # long_period = 14

        sma_short_curr = sum(closes[-short_period:]) / short_period
        sma_long_curr = sum(closes[-long_period:]) / long_period

        sma_short_prev = sum(closes[-short_period-1:-1]) / short_period
        sma_long_prev = sum(closes[-long_period-1:-1]) / long_period
        print(str(sma_short_curr) + " short curr")
        print(str(sma_short_prev) + " short prev")
        print(str(sma_long_curr) + " long curr")
        print(str(sma_long_prev) + " long prev")
        # Check for a bullish crossover 
        if sma_short_curr > sma_long_curr and sma_short_prev <= sma_long_curr:
            print("Bullish crossover detected!")

    def first_candle(self):
        current_row = self.dataframe.tail(1)
    # Need ATR Calculation, Volume Calculation, etc.
    
    def get_data_frame(self):
        return self.dataframe
