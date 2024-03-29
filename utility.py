import argparse 
import time 
import socket
import numpy as np
import pandas as pd

def create_parser():
    parser = argparse.ArgumentParser(description="Arguments: data_retrieval, indicator, knn_evaluation, bot_indicator")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('data_retrieval', help='Retrieves historical crypto data')
    subparsers.add_parser('indicator', help='Uses knn to predict an increase or decrease')
    subparsers.add_parser('knn_evaluation', help='Tests the knn prediction accuracy')
    subparsers.add_parser('bot_indicator', help='Starts discord bot that uses indicator to predict when to buy and sell')
    parser.add_argument("-c", "--coded_model", action="store_true", help="Doesn't use the sklearn library for prediction")
    parser.add_argument("-s", "--sklearn_model", action="store_true", help="Uses the sklearn library for prediction")
    args = parser.parse_args()

    return args

def check_internet_connection():
    while True:
        try:
            sock = socket.create_connection(("www.google.com", 80) , 5)
            if sock is not None: 
                sock.close 
                print("Connected to the Internet.")
                return True
        except OSError: 
            print("No internet connection. Retrying in 5 seconds...")
            time.sleep(5)
            continue
distances = []
def euclidean_distance(x1, x2):
    distance = np.sqrt(np.sum((x2 -x1)**2))
    distances.append(distance)
    return distance