import pandas as pd
import numpy as np
from IPython.display import display

crypto_data = pd.read_csv("bitcoin_data.csv")
crypto_data["Fast_Average"] = crypto_data["Close"].rolling(7).mean()
crypto_data["Slow_Average"] = crypto_data["Close"].rolling(14).mean()
crypto_data["Prev_Fast"] = crypto_data["Fast_Average"].shift(1)
crypto_data["Prev_Slow"] = crypto_data["Slow_Average"].shift(1)
crypto_data["Volume Change"] = crypto_data["Volume"].pct_change(7)

def ATR_calculation():
    high_low = crypto_data['High'] - crypto_data['Low']
    high_close = abs(crypto_data['High'] - crypto_data['Close'].shift())
    low_close = abs(crypto_data['Low'] - crypto_data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    crypto_data["ATR"] = true_range.rolling(14).sum()/14

ATR_calculation()

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

def profit_calculation():
    profit_column = []
    profit_values = []
    bear_indexes = []

    for index, row in crypto_data.iterrows():
        if row["Crossover"] == "Bull":
            bear_index = index + 1
            while bear_index < len(crypto_data) and crypto_data.loc[bear_index, "Crossover"] != "Bear":
                bear_index += 1
            if bear_index < len(crypto_data):
                profit = crypto_data.loc[bear_index, "Close"] - row["Close"]
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

    crypto_data["Profit"] = profit_column
    crypto_data["Profit Values"] = profit_values
    crypto_data["Bear Index"] = bear_indexes

profit_calculation() 
print(crypto_data["Profit Values"].sum())

count = crypto_data["Profit"].value_counts()
print(count)
increase_ratio = count["Increase"] / count.sum()
print(increase_ratio * 100)

entry_price = 0
trailing_stop_loss = 0
stop_loss_index = None
multiplier = 1
crypto_data["Exit Price"] = ""
crypto_data["Profit/Loss"] = 0
crypto_data["Profit Indicator"] = ""

bullish_index = None

for index, row in crypto_data.iterrows():
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
            crypto_data.at[bullish_index, "Exit Price"] = trailing_stop_loss
            crypto_data.at[bullish_index, "Profit/Loss"] = profit_loss 
            crypto_data.at[bullish_index, "Profit Indicator"] = "Decrease" if profit_loss < 0 else "Increase"
            bullish_index = None

        if row["Low"] <= trailing_stop_loss:
            profit_loss = trailing_stop_loss - entry_price
            crypto_data.at[bullish_index, "Profit/Loss"] = profit_loss
            crypto_data.at[bullish_index, "Profit Indicator"] = "Decrease" if profit_loss < 0 else "Increase"
            stop_loss_index = index
        else:
            profit_loss = row["Close"] - entry_price
            crypto_data.at[bullish_index, "Profit/Loss"] = profit_loss
            crypto_data.at[bullish_index, "Profit Indicator"] = "Increase" if profit_loss >= 0 else "Decrease"
            crypto_data.at[bullish_index, "Index"] = index

        bullish_index = None


print(crypto_data["Profit/Loss"].sum())


def new_csv():
    global crypto_data
    crypto_data = crypto_data[crypto_data["Crossover"].isin(["Bull"])]
    delete_columns = ['Open time','Close time', 'Quote asset volume', 'Number of trades','Ignore']
    crypto_data = crypto_data.drop(delete_columns, axis = 1)
    # crypto_data.dropna(inplace=True)
    crypto_data.to_csv("bitcoin_data_V3.csv")

new_csv()