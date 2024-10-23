from src.data_preprocessing import preprocess_new_data
import joblib
from tensorflow.keras.models import load_model

def predict_match(team_1, team_2, team_1_odds, team_2_odds, model_type='logistic'):
    # Preprocess new match data
    new_match = preprocess_new_data(team_1, team_2, team_1_odds, team_2_odds)

    # Load the appropriate model
    if model_type == 'logistic':
        model = joblib.load('models/logistic_model.pkl')
        prediction = model.predict(new_match)
    elif model_type == 'nn':
        model = load_model('models/nn_model.h5')
        prediction = model.predict(new_match)
        prediction = 1 if prediction > 0.5 else 0  # Convert NN probability to binary
    
    if prediction == 1:
        print(f"Prediction: {team_1} will win!")
    else:
        print(f"Prediction: {team_2} will win!")

# Example prediction for Griffins vs Avalanche
predict_match('Griffins', 'Avalanche', 1.6, 1.8, model_type='logistic')
