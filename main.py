from bot import start_bot, trade_identifier
from binance.client import Client
from historical import CryptoDataRetrieval
from crossover import Analyze
from knn import KNN
from trade import CryptoTrade
from datetime import datetime
import asyncio
import utility

symbol = 'BTCUSDT'
short_period = 7
long_period = 14

# Data Retrieval
def data_retrieval():
    crypto_data = CryptoDataRetrieval(symbol, Client.KLINE_INTERVAL_1HOUR, datetime(2020, 1, 1), datetime(2022, 5, 20))
    crypto_data.data_retrieval()

# KNN Accuracy 
def knn_evaluation(args):
    data_modifier = Analyze(file="bitcoin_data.csv")
    data_modifier.averages(short_period, long_period)
    data_modifier.volume_calculation()
    data_modifier.ATR_calculation(long_period)
    data_modifier.calculate_rsi(long_period)
    data_modifier.drop_null()
    data_modifier.crossover_detection()
    data_modifier.ATR_trailing_stop_loss()
    data_modifier.save_as_csv("bitcoin_data_V4.csv")
    knn_accuracy = KNN(filename="bitcoin_data_V4.csv", k=45)
    preprocess = knn_accuracy.preprocess()
    if args.sklearn_model:
        model = knn_accuracy.model_train(preprocess[0], preprocess[2])
        knn_accuracy.evaluate2(model, preprocess[1], preprocess[3])
    elif args.coded_model:
        prediction = knn_accuracy.predict(preprocess[1], preprocess[0])
        knn_accuracy.evaluate(prediction, preprocess[3])
    

def indicator(args):
    #Trade Identifier
    trade = CryptoTrade(symbol, Client.KLINE_INTERVAL_1WEEK, long_period + 1)
    trade.dataframe_creation()
    if True: #trade.bullish_crossover(short_period, long_period) == ("Bullish"): 
        trade_dataframe = trade.get_data_frame()
        dataframe_addition = Analyze(dataframe=trade_dataframe)
        dataframe_addition.averages(short_period, long_period)
        dataframe_addition.volume_calculation()
        dataframe_addition.ATR_calculation(long_period)
        dataframe_addition.calculate_rsi(long_period)
        dataframe_addition.drop_null()
        data = dataframe_addition.get_dataframe()
        knn_prediction = KNN(filename="bitcoin_data_V4.csv", k=45)
        trade_preprocess = knn_prediction.preprocess()
        processed_data = knn_prediction.preprocess_single(data)
        prediction = None
        if args.sklearn_model:
            model = knn_prediction.model_train(trade_preprocess[0], trade_preprocess[2])
            prediction = knn_prediction.current_predict(processed_data, model)
        elif args.coded_model:
            prediction = knn_prediction.predict(processed_data, trade_preprocess[0])
        return(str(prediction[0]))
    else:
        return("Neither")
    
async def periodic_notification(args):
    result = "Neither"
    stoploss_start = False
    while True:
        current_time = datetime.now()
        if current_time.minute == 0 and stoploss_start == False:
            result = indicator(args)
            stoploss_price = calculate_ATR_stoploss_hourly(stoploss_start)
            if result == "Increase":
                stoploss_start = True
                await (trade_identifier(result, symbol))
        elif current_time.second == 0 and stoploss_start == True:
            current_price = calculate_ATR_stoploss_hourly(stoploss_start)
            if stoploss_price > current_price:
                stoploss_start = False
                result = "Sell"
                await (trade_identifier(result, symbol))
        await asyncio.sleep(1)

async def start(args):
    bot_start = asyncio.create_task(start_bot())
    await asyncio.sleep(1)
    message = asyncio.create_task(periodic_notification(args))
    await asyncio.gather(bot_start, message)

def calculate_ATR_stoploss_hourly(stoploss_start):
    trade = CryptoTrade(symbol, Client.KLINE_INTERVAL_1WEEK, long_period + 1)
    trade.dataframe_creation()
    trade_dataframe = trade.get_data_frame()
    dataframe_addition = Analyze(dataframe=trade_dataframe)
    dataframe_addition.ATR_calculation(long_period)
    dataframe_addition.drop_null()
    dataframe = dataframe_addition.get_dataframe()
    trailing_stop_loss = dataframe.at[14, "Close"] - (0.9 * dataframe.at[14, "ATR"])
    if stoploss_start == True:
        return trailing_stop_loss
    else:
        return dataframe.at[14, "Close"]

def main():
    args = utility.create_parser()
    if args.command == 'data_retrieval':
        data_retrieval()
    elif args.command == 'indicator':
        indicator(args)
    elif args.command == 'knn_evaluation':
            knn_evaluation(args)
    elif args.command == 'bot_indicator':
        if not utility.check_internet_connection():
            print("Cannot establish internet connection. Exiting...")
            return
        asyncio.run(start(args))
    

if __name__ == "__main__":
    main()