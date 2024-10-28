import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import joblib

# Loading Data
# Function to load all CSV files from a directory structure for a specific race.
def load_all_data(root_dir, race_location=None):
    dataframes = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv'):
                if race_location is None or race_location in root:
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# Option to load data for all Grand Prix events or a specific one
root_data_dir = './data/drivers/'
load_all = True  # Set to True to load all data, False to load specific race data
race_location = 'great_britain'  # Change this if needed

# Load data accordingly
if load_all:
    data = load_all_data(root_data_dir)
else:
    data = load_all_data(root_data_dir, race_location)

# Data Preprocessing
# Inspect the available columns
print("Columns in dataset:", data.columns)

# Identify common columns across all dataframes
common_columns = data.columns

# Update feature selection based on available columns
# Automatically select common numeric features for training
features = [
    col for col in common_columns
    if col not in ['position', 'date', 'driver_number', 'meeting_key', 'session_key', 'driver_name']
    and data[col].dtype in ['int64', 'float64']
]
label = 'position'

# Handling Missing Values
numeric_columns = data.select_dtypes(include=['number']).columns
if not numeric_columns.empty:
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Encoding Categorical Variables
encoder = LabelEncoder()
if label in data.columns and data[label].dtype == 'object':
    data[label] = encoder.fit_transform(data[label])

# Add historical average position as a feature
if 'driver_number' in data.columns and 'position' in data.columns:
    data['average_position'] = data.groupby('driver_number')['position'].transform('mean')
    features.append('average_position')

# Convert label to discrete categories if it's continuous
if data[label].dtype != 'int' and data[label].dtype != 'object':
    data[label] = pd.qcut(data[label], q=4, labels=False, duplicates='drop')

# Check if selected features and label exist in data
if features and label in data.columns:
    # Splitting Data for Training and Testing
    X = data[features]
    y = data[label]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardizing the Data
    scaler = StandardScaler()
    if not X_train.size == 0:
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Building the Model
        model = RandomForestClassifier(
            n_estimators=200,
            criterion='gini',
            max_depth=15,
            random_state=42
        )

        # Training the Model
        model.fit(X_train, y_train)

        # Evaluating the Model
        y_pred = model.predict(X_test)

        conf_matrix = confusion_matrix(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print("Confusion Matrix:")
        print(conf_matrix)
        print("\nAccuracy:", accuracy)
        print("\nClassification Report:")
        print(report)

        # Saving the Model for Predictions
        joblib.dump(model, f'./models/{race_location.replace(" ", "_") if not load_all else "all_gp"}_gp_predictor_model.pkl')
        joblib.dump(scaler, './models/scaler.pkl')
    else:
        print("Error: Training data is empty. Please check the feature selection and data loading steps.")
else:
    print("Error: One or more features or the label column are not present in the dataset.")
