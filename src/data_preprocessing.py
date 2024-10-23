import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)
    
    data = data.dropna()

    X = data.drop('result', axis=1)
    y = data['result']

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test
