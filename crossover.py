import pandas as pd
import numpy as np
from IPython.display import display

crypto_data = pd.read_csv("bitcoin_data.csv")
crypto_data["Fast_Average"] = crypto_data["Close"].rolling(7).mean()
crypto_data["Slow_Average"] = crypto_data["Close"].rolling(14).mean()
crypto_data["Prev_Fast"] = crypto_data["Fast_Average"].shift(1)
crypto_data["Prev_Slow"] = crypto_data["Slow_Average"].shift(1)

crypto_data["Volume Change"] = crypto_data["Volume"].pct_change(7)

high_low = crypto_data['High'] - crypto_data['Low']
high_close = abs(crypto_data['High'] - crypto_data['Close'].shift())
low_close = abs(crypto_data['Low'] - crypto_data['Close'].shift())
ranges = pd.concat([high_low, high_close, low_close], axis=1)
true_range = np.max(ranges, axis=1)
crypto_data["ATR"] = true_range.rolling(14).sum()/14

import pandas as pd

def calculate_rsi(data, window=14):
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)

    avg_gain = up.rolling(window).mean()
    avg_loss = down.rolling(window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

crypto_data['RSI'] = calculate_rsi(crypto_data['Close'])


crypto_data.dropna(inplace=True)

def crossover_finder(prev_fast, fast, slow):
    if((fast > slow) and (prev_fast < slow)):
        return "Bull"
    elif((fast < slow) and (prev_fast > slow)):
        return "Bear"
    return "Neither"

crypto_data["Crossover"] = np.vectorize(crossover_finder)(crypto_data["Prev_Fast"], crypto_data["Fast_Average"], crypto_data["Slow_Average"])


profit_column = []

for index, row in crypto_data.iterrows():
    if row["Crossover"] == "Bull":
        bear_index = index + 1
        while bear_index < len(crypto_data) and crypto_data.loc[bear_index, "Crossover"] != "Bear":
            bear_index += 1
        if bear_index < len(crypto_data):
            profit = crypto_data.loc[bear_index, "Close"] - row["Close"]
            if profit < 0:
                profit_column.append("Decrease")
            else:
                profit_column.append("Increase")
        else:
            profit_column.append("Neither")
    else:
        profit_column.append("Neither")

crypto_data["Profit"] = profit_column
crypto_data = crypto_data[crypto_data["Crossover"].isin(["Bull"])]
delete_columns = ['Open time','Close time', 'Quote asset volume', 'Number of trades','Ignore']
crypto_data = crypto_data.drop(delete_columns, axis = 1)
crypto_data.to_csv("bitcoin_data_V2.csv")