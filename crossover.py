import pandas as pd
import numpy as np
from IPython.display import display

class Analyze:
    def __innit__(self, file=None, dataframe=None):
        if file:
            self.crypto_data = pd.read_csv(file)
        elif dataframe is not None:
            self.crypto_data = dataframe
        else:
            self.crypto_data = None

    def averages(self, short_period, long_period):
        self.crypto_data = pd.read_csv("bitcoin_data.csv")
        self.crypto_data["Fast_Average"] = self.crypto_data["Close"].rolling(short_period).mean()
        self.crypto_data["Slow_Average"] = self.crypto_data["Close"].rolling(long_period).mean()
        self.crypto_data["Prev_Fast"] = self.crypto_data["Fast_Average"].shift(1)
        self.crypto_data["Prev_Slow"] = self.crypto_data["Slow_Average"].shift(1)
        self.crypto_data["Volume Change"] = self.crypto_data["Volume"].pct_change(7)

    def ATR_calculation(self, period):
        high_low = self.crypto_data['High'] - self.crypto_data['Low']
        high_close = np.abs(self.crypto_data['High'] - self.crypto_data['Close'].shift())
        low_close = np.abs(self.crypto_data['Low'] - self.crypto_data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        self.crypto_data["ATR"] = true_range.rolling(period).sum()/period

    ATR_calculation(14)

    def calculate_rsi(self, window):
        delta = self.crypto_data['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)

        avg_gain = up.rolling(window).mean()
        avg_loss = down.rolling(window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        self.crypto_data['RSI'] = rsi

    calculate_rsi(14)

    def drop_null(self):
        self.crypto_data.dropna(inplace=True)

    def crossover_detection(self):
        def crossover_finder(prev_fast, fast, slow):
            if((fast > slow) and (prev_fast < slow)):
                return "Bull"
            elif((fast < slow) and (prev_fast > slow)):
                return "Bear"
            return "Neither"

        self.crypto_data["Crossover"] = np.vectorize(crossover_finder)(self.crypto_data["Prev_Fast"], self.crypto_data["Fast_Average"], self.crypto_data["Slow_Average"])

    def profit_calculation(self):
        profit_column = []
        profit_values = []
        bear_indexes = []

        for index, row in self.crypto_data.iterrows():
            if row["Crossover"] == "Bull":
                bear_index = index + 1
                while bear_index < len(self.crypto_data) and self.crypto_data.loc[bear_index, "Crossover"] != "Bear":
                    bear_index += 1
                if bear_index < len(self.crypto_data):
                    profit = self.crypto_data.loc[bear_index, "Close"] - row["Close"]
                    if profit < 0:
                        profit_column.append("Decrease")
                        profit_values.append(profit)
                        bear_indexes.append(bear_index)
                    else:
                        profit_column.append("Increase")
                        profit_values.append(profit)
                        bear_indexes.append(bear_index)
                else:
                    profit_column.append(None)
                    profit_values.append(None)
                    bear_indexes.append(None)
            else:
                profit_column.append(None)
                profit_values.append(None)
                bear_indexes.append(None)

        self.crypto_data["Profit"] = profit_column
        self.crypto_data["Profit Values"] = profit_values
        self.crypto_data["Bear Index"] = bear_indexes

    profit_calculation() 
    
    def display_profit(self, profit_values, profit_indicator):
        print(self.crypto_data[profit_values].sum())

        count = self.crypto_data[profit_indicator].value_counts()
        print(count)
        increase_ratio = count["Increase"] / count.sum()
        print(increase_ratio * 100)

    display_profit("Profit Values", "Profit")
    
    def ATR_trailing_stop_loss(self):
        entry_price = 0
        trailing_stop_loss = 0
        stop_loss_index = None
        multiplier = .9
        self.crypto_data["Exit Price"] = ""
        self.crypto_data["Profit/Loss"] = 0
        self.crypto_data["Profit Indicator"] = None

        bullish_index = None

        for index, row in self.crypto_data.iterrows():
            if row["Crossover"] == "Bull":
                if bullish_index is None:
                    entry_price = row["Close"]
                    atr = row["ATR"]
                    trailing_stop_loss = entry_price
                    bullish_index = index
                    trailing_stop_loss = entry_price - (multiplier * atr)
            elif bullish_index is not None:
                atr = row["ATR"]
                trailing_stop_loss = row["Open"] - (multiplier * atr)
                if row["Low"] <= trailing_stop_loss:
                    profit_loss = trailing_stop_loss - entry_price 
                    self.crypto_data.at[bullish_index, "Exit Price"] = trailing_stop_loss
                    self.crypto_data.at[bullish_index, "Profit/Loss"] = profit_loss 
                    self.crypto_data.at[bullish_index, "Profit Indicator"] = "Decrease" if profit_loss < 0 else "Increase"
                    bullish_index = None
                    
    ATR_trailing_stop_loss()
    display_profit("Profit/Loss", "Profit Indicator")


    def save_as_csv(self, filename):
        crypto_data = crypto_data[crypto_data["Crossover"].isin(["Bull"])]
        delete_columns = ['Open time','Close time', 'Quote asset volume', 'Number of trades','Ignore', 'Profit']
        crypto_data = crypto_data.drop(delete_columns, axis = 1)
        crypto_data.dropna(inplace=True)
        crypto_data.to_csv(filename)

    save_as_csv("bitcoin_data_V3.csv")