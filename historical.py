from binance.client import Client
from datetime import datetime
from dotenv import load_dotenv
import csv
import os

filename = 'bitcoin_data.csv'
api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

client = Client(api_key, api_secret)

symbol = 'BTCUSDT'  
timeframe = Client.KLINE_INTERVAL_1HOUR 

start_time = datetime(2018, 1, 1)  
end_time = datetime(2022, 5, 20) 

start_timestamp = int(start_time.timestamp() * 1000)  
end_timestamp = int(end_time.timestamp() * 1000) 

historical_data = client.get_historical_klines(symbol, timeframe, start_timestamp, end_timestamp)

for row in historical_data:
    row[0] = int(row[0]/1000)

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for data_row in historical_data:
        writer.writerow(data_row)