import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler


# Assuming you have a DataFrame 'crypto_data' with features and target column
crypto_data = pd.read_csv("bitcoin_data_V2.csv")


exclude_columns = ['Timestamp']
numeric_columns = [column for column in crypto_data.columns if column not in exclude_columns and crypto_data[column].dtype != 'object']
X = crypto_data[numeric_columns].copy()

# Apply scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

y = crypto_data['Profit']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the k-NN classifier
knn = KNeighborsClassifier(n_neighbors=65)

# Train the model
knn.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

