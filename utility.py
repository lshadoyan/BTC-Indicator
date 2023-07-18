import argparse 
import time 
import subprocess

def create_parser():
    parser = argparse.ArgumentParser(description="Arguments: data_retrieval, indicator, knn_evaluation, bot_indicator")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('data_retrieval', help='Retrieves historical crypto data')
    subparsers.add_parser('indicator', help='Uses knn to predict an increase or decrease')
    subparsers.add_parser('knn_evaluation', help='Tests the knn prediction accuracy')
    subparsers.add_parser('bot_indicator', help='Starts discord bot that uses indicator to predict when to buy and sell')
    args = parser.parse_args()
    return args

def check_internet_connection():
    while True:
        try:
            response = subprocess.run(['ping', '-n', '1', 'google.com'], capture_output=True)
            if response.returncode == 0:
                print("Connected to the internet.")
                return True
            else:
                print("No internet connection. Retrying in 5 seconds...")
                time.sleep(5)
                continue
        except subprocess.CalledProcessError:
            print("No internet connection. Retrying in 5 seconds...")
            time.sleep(5)
            return False