from binance.client import Client
from dotenv import load_dotenv
import csv
import os

load_dotenv()
header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
filename = 'bitcoin_data.csv'
api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

class CryptoDataRetrieval:
    def __init__(self, currency, time_frame, start_time, end_time):
        self.symbol = currency 
        self.timeframe = time_frame 
        self.start_timestamp = int(start_time.timestamp() * 1000) 
        self.end_timestamp = int(end_time.timestamp() * 1000) 

    def data_retrieval(self):
        try:
            client = Client(api_key, api_secret)  
            historical_data = client.get_historical_klines(self.symbol, self.timeframe, self.start_timestamp, self.end_timestamp)

            for row in historical_data:
                row[0] = int(row[0]/1000)

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                for data_row in historical_data:
                    writer.writerow(data_row)
        except Exception as e:
            print(f"Error occurred during data retrieval: {str(e)}")