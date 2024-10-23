from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def train_logistic_regression(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Logistic Regression Model Accuracy: {accuracy * 100:.2f}%")

def save_model(model, filename='models/logistic_model.pkl'):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")
