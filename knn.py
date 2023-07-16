import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

class KNN:
    def __init__(self, filename):
            self.crypto_data = pd.read_csv(filename)

    def preprocess(self):
        exclude_columns = ['Timestamp', "Exit Price", "Profit/Loss", "Profit Values", "Bear Index", "Profit", 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Exit Price', 'Unnamed: 0', 'Start Price', 'Middle Price', 'End Price']
        numeric_columns = [column for column in self.crypto_data.columns if column not in exclude_columns and self.crypto_data[column].dtype != 'object']
        
        X = self.crypto_data[numeric_columns].copy()
        y = self.crypto_data["Profit Indicator"]

        X = self.scale_data(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test
    
    def scale_data(self, X):
         mean = np.mean(X, axis=0)
         std = np.std(X, axis=0)
         X_scaled = (X - mean) / std
         return X_scaled
    
    def model_train(self, X_train, y_train):

        knn = KNeighborsClassifier(n_neighbors=30)

        knn.fit(X_train, y_train)

        return knn

    def evaluate(self, model, X_test, y_test):
        y_pred = model.predict(X_test)
        print(y_pred)

        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

    def predict(self, dataframe, model):
        exclude_columns = ['Unnamed: 0', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Exit Price', 'Profit/Loss']
        numeric_columns = [column for column in self.crypto_data.columns if column not in exclude_columns and self.crypto_data[column].dtype != 'object']
        X = dataframe[numeric_columns].copy()
        
        X_scaled = self.scale_data(X)
        
        prediction = model.predict(X_scaled)
        
        return prediction

