import pandas as pd
import numpy as np

crypto_data = pd.read_csv("bitcoin_data.csv")

crypto_data["Fast_Average"] = crypto_data["Close"].rolling(50).mean()
crypto_data["Slow_Average"] = crypto_data["Close"].rolling(200).mean()
crypto_data["Prev_Fast"] = crypto_data["Fast_Average"].shift(1)
crypto_data.dropna(inplace=True)

def crossover_finder(prev_fast, fast, slow):
    if((fast > slow) and (prev_fast < slow)):
        return "Bull"
    elif((fast > slow) and (prev_fast > slow)):
        return "Bear"
    return None
crypto_data["Crossover"] = np.vectorize(crossover_finder)(crypto_data["Prev_Fast"], crypto_data["Fast_Average"], crypto_data["Slow_Average"])

