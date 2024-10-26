import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the saved model and scaler
model = joblib.load('models/mexican_gp_predictor_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Sample Prediction
def predict_position(sample_data):
    sample_data = scaler.transform(sample_data)
    position_prediction = model.predict(sample_data)
    return position_prediction

if __name__ == "__main__":
    sample_data = np.array([[10, 250, 25, 1, 40, 22]])  # Sample lap data (lap, speed, pit_time, stint, track_temp, air_temp)
    predicted_position = predict_position(sample_data)
    print("Predicted Position:", predicted_position)