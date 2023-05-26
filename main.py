from binance.client import Client
from historical import CryptoDataRetrieval
from datetime import datetime

def main():
    crypto_data = CryptoDataRetrieval('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, datetime(2018, 1, 1), datetime(2022, 5, 20))
    crypto_data.data_retrieval()


if __name__ == "__main__":
    main()