from src.data_preprocessing import load_and_preprocess_data, preprocess_new_data
from src.logistic_regression_model import (
    train_logistic_regression,
    evaluate_model as evaluate_logistic,
    save_model as save_logistic,
)
from src.neural_network_model import (
    train_neural_network,
    plot_training_history,
    save_model as save_nn,
)
from src.utils import create_directory
import joblib
from tensorflow.keras.models import load_model

# Load and preprocess data
X_train, X_test, y_train, y_test = load_and_preprocess_data('data/sports_data.csv')

# Create models directory
create_directory('models')

# Train and evaluate logistic regression model
logistic_model = train_logistic_regression(X_train, y_train)
evaluate_logistic(logistic_model, X_test, y_test)
save_logistic(logistic_model)

# Train and evaluate neural network model
nn_model, history = train_neural_network(X_train, y_train, epochs=10)
plot_training_history(history)
save_nn(nn_model)

# --- New Section for Predicting Match Outcomes ---

def predict_match(team_1, team_2, team_1_odds, team_2_odds, model_type='logistic'):
    new_match = preprocess_new_data(team_1, team_2, team_1_odds, team_2_odds)

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

predict_match('Griffins', 'Avalanche', 1.6, 1.8, model_type='logistic')
predict_match('Griffins', 'Avalanche', 1.6, 1.8, model_type='nn')
