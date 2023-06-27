from binance.client import Client
from historical import CryptoDataRetrieval
from crossover import Analyze
from knn import KNN
from trade import CryptoTrade
from datetime import datetime

def main():
    #Data Retrieval
    # crypto_data = CryptoDataRetrieval('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, datetime(2020, 1, 1), datetime(2022, 5, 20))
    # crypto_data.data_retrieval()

    #KNN Accuracy 
    data_modifier = Analyze(file="bitcoin_data.csv")
    data_modifier.averages()
    data_modifier.volume_calculation()
    data_modifier.ATR_calculation()
    data_modifier.calculate_rsi()
    data_modifier.drop_null()
    data_modifier.crossover_detection()
    data_modifier.ATR_trailing_stop_loss()
    data_modifier.save_as_csv("bitcoin_data_V4.csv")
    knn_accuracy = KNN("bitcoin_data_V4.csv")
    preprocess = knn_accuracy.preprocess()
    model = knn_accuracy.model_train(preprocess[0], preprocess[2])
    knn_accuracy.evaluate(model, preprocess[1], preprocess[3])


    #Trade Identifier

if __name__ == "__main__":
    main()