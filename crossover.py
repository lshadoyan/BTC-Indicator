import pandas as pd
import numpy as np
from IPython.display import display

crypto_data = pd.read_csv("bitcoin_data.csv")
crypto_data["Fast_Average"] = crypto_data["Close"].rolling(7).mean()
crypto_data["Slow_Average"] = crypto_data["Close"].rolling(14).mean()
crypto_data["Prev_Fast"] = crypto_data["Fast_Average"].shift(1)
crypto_data["Prev_Slow"] = crypto_data["Slow_Average"].shift(1)
crypto_data.dropna(inplace=True)

def crossover_finder(prev_fast, fast, slow):
    if((fast > slow) and (prev_fast < slow)):
        return "Bull"
    elif((fast < slow) and (prev_fast > slow)):
        return "Bear"
    return "Neither"

crypto_data["Crossover"] = np.vectorize(crossover_finder)(crypto_data["Prev_Fast"], crypto_data["Fast_Average"], crypto_data["Slow_Average"])

crypto_data["Profit"] = "Neither"

for index_bull in range(len(crypto_data)):
    if crypto_data.iloc[index_bull]["Crossover"] == "Bull":
        index_bear = index_bull + 1
        while index_bear < len(crypto_data) and crypto_data.iloc[index_bear]["Crossover"] != "Bull":
            index_bear += 1
        if index_bear < len(crypto_data):
            profit = crypto_data.iloc[index_bear]["Close"] - crypto_data.iloc[index_bull]["Close"]
            if profit < 0:
                crypto_data.at[index_bull, 'Profit'] = "Decrease"
            else:
                crypto_data.at[index_bull, 'Profit'] = "Increase"
        