import pandas as pd

crypto_data = pd.read_csv("bitcoin_data.csv")
crypto_data["Fast_Average"] = crypto_data["Close"].rolling(50).mean()
crypto_data["Slow_Average"] = crypto_data["Close"].rolling(200).mean()
