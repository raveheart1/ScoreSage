import joblib
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load the saved model and scaler
model = joblib.load('models/all_gp_gp_predictor_model.pkl')  # Use the latest model path
scaler = joblib.load('models/scaler.pkl')

# Function to load and merge position data with stint, pit, and other available data
def load_and_merge_data(root_dir):
    dataframes = []
    for driver in os.listdir(root_dir):
        driver_path = os.path.join(root_dir, driver)
        if os.path.isdir(driver_path):
            grand_prix_path = os.path.join(driver_path, 'grand-prix')
            if os.path.isdir(grand_prix_path):
                for race in os.listdir(grand_prix_path):
                    race_folder_path = os.path.join(grand_prix_path, race)
                    if os.path.isdir(race_folder_path):
                        try:
                            # Load position data
                            position_data_path = os.path.join(race_folder_path, 'position_data_Race.csv')
                            if os.path.exists(position_data_path):
                                position_df = pd.read_csv(position_data_path)

                                # Load and merge stint data if available
                                stint_data_path = os.path.join(race_folder_path, 'stints_data_Race.csv')
                                if os.path.exists(stint_data_path):
                                    stint_df = pd.read_csv(stint_data_path)
                                    merge_keys = [key for key in ['date', 'session_key'] if key in position_df.columns and key in stint_df.columns]
                                    if merge_keys:
                                        position_df = position_df.merge(stint_df, on=merge_keys, how='left')
                                    else:
                                        print(f"Warning: Could not merge stint data for {race_folder_path} due to missing keys.")

                                # Load and merge pit data if available
                                pit_data_path = os.path.join(race_folder_path, 'pit_data_Race.csv')
                                if os.path.exists(pit_data_path):
                                    pit_df = pd.read_csv(pit_data_path)
                                    merge_keys = [key for key in ['date', 'session_key'] if key in position_df.columns and key in pit_df.columns]
                                    if merge_keys:
                                        position_df = position_df.merge(pit_df, on=merge_keys, how='left')
                                    else:
                                        print(f"Warning: Could not merge pit data for {race_folder_path} due to missing keys.")

                                # Add driver name for context
                                position_df['driver_name'] = driver

                                # Add to dataframes list
                                dataframes.append(position_df)
                            else:
                                print(f"Warning: No position data found at {position_data_path}")

                        except Exception as e:
                            print(f"Warning: Failed to read data from {race_folder_path}. Error: {e}")

    if not dataframes:
        print("Error: No valid CSV files found in the specified directory structure.")
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

# Prediction and comparison function
def predict_and_compare_all(root_data_dir):
    # Load and merge all drivers' data
    data = load_and_merge_data(root_data_dir)

    # Check if data is empty
    if data.empty:
        print("Error: No data available for prediction. Please check the dataset paths.")
        return

    # Print columns to verify what data is available
    print("Available columns in the data:", data.columns)

    # Extract features and label
    # Automatically select numeric columns that are not specifically excluded
    features = [
        col for col in data.columns
        if col not in ['position', 'date', 'driver_number', 'meeting_key', 'session_key', 'driver_name']
        and pd.api.types.is_numeric_dtype(data[col])
    ]

    # Print out the features that are being selected
    print("Selected features:", features)

    if not features:
        print("Error: No valid features found in the data. Please ensure there are numeric columns available for feature extraction.")
        return

    X = data[features]
    y_actual = data['position']

    # Standardize features
    X_scaled = scaler.transform(X)

    # Make predictions
    y_pred = model.predict(X_scaled)

    # Compare predictions vs actual labels
    print("Predicted vs Actual:")
    for actual, predicted, driver in zip(y_actual, y_pred, data['driver_name']):
        print(f"Driver: {driver}, Actual: {actual}, Predicted: {predicted}")

    # Evaluate model performance
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_actual, y_pred))
    print("\nAccuracy:", accuracy_score(y_actual, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_actual, y_pred))

if __name__ == "__main__":
    # Path to the dataset directory containing all drivers' data
    root_data_dir = './data/drivers/'  # Root directory containing each driver's folder
    predict_and_compare_all(root_data_dir)
