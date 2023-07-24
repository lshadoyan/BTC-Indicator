import pandas as pd
import numpy as np
import utility
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from collections import Counter
from tqdm import tqdm

mean = 0
std = 0
class KNN:
    def __init__(self, filename, k):
            self.crypto_data = pd.read_csv(filename)
            self.k = k

    def preprocess(self):
        exclude_columns = ['Timestamp', "Exit Price", "Profit/Loss", "Profit Values", "Bear Index", "Profit", 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Exit Price', 'Unnamed: 0', 'Start Price', 'Middle Price', 'End Price']
        numeric_columns = [column for column in self.crypto_data.columns if column not in exclude_columns and self.crypto_data[column].dtype != 'object']
        
        self.X = self.crypto_data[numeric_columns].copy()
        self.y = self.crypto_data["Profit Indicator"]
        self.X = self.scale_data(self.X, False)

        X_train, X_test, y_train, y_test = self.split_data(self.X, self.y, test_size=0.2, random_state=12)
        return X_train, X_test, y_train, y_test
    
    def scale_data(self, X, single):
        global mean, std
        if single:
            X_scaled = (X - mean) / std
        else:
            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)
            X_scaled = (X - mean) / std
        return X_scaled
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        num_samples = len(X)
        num_test_samples = int(num_samples * test_size)
        num_train_samples = num_samples - num_test_samples

        np.random.seed(random_state)

        indices = np.random.permutation(num_samples)
        train_indices = indices[:num_train_samples]
        test_indices = indices[num_train_samples:]

        X_train = X.iloc[train_indices]
        X_test = X.iloc[test_indices]
        y_train = y.iloc[train_indices]
        y_test = y.iloc[test_indices]

        return X_train, X_test, y_train, y_test
    
    def predict(self, X_test, X_train):
         predict = [self._predict(x, X_train) for x in tqdm(X_test.itertuples(index=False), total=len(X_test))]
        #  utility.print_distances()
         return predict

    def _predict(self, x, X_train):
         distances = [utility.euclidean_distance(x, x_train) for index, x_train in X_train.iterrows()]
         k_near = np.argsort(distances)[:self.k]
         y_label = [self.y[i] for i in k_near]
         y_common = Counter(y_label).most_common(1)
         return y_common[0][0]
    
    def model_train(self, X_train, y_train):

        knn = KNeighborsClassifier(n_neighbors=self.k)

        knn.fit(X_train, y_train)

        return knn

    def evaluate(self, y_pred, y_test):

        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
    
    def evaluate2(self, model, X_test, y_test):
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

    def current_predict(self, dataframe, model):
        prediction = model.predict(dataframe)

        return prediction
    
    def preprocess_single(self, dataframe):
        exclude_columns = ['Timestamp','Unnamed: 0', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Exit Price', 'Profit/Loss', 'Start Price', 'Middle Price', 'End Price']
        numeric_columns = [column for column in dataframe.columns if column not in exclude_columns and dataframe[column].dtype != 'object']
        X = dataframe[numeric_columns].copy()
        X_scaled = self.scale_data(X, True)
        return X_scaled

