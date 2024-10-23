from src.data_preprocessing import load_and_preprocess_data
from src.logistic_regression_model import train_logistic_regression, evaluate_model as evaluate_logistic, save_model as save_logistic
from src.neural_network_model import train_neural_network, plot_training_history, save_model as save_nn
from src.utils import create_directory

X_train, X_test, y_train, y_test = load_and_preprocess_data('data/sports_data.csv')

create_directory('models')

logistic_model = train_logistic_regression(X_train, y_train)
evaluate_logistic(logistic_model, X_test, y_test)
save_logistic(logistic_model)

nn_model, history = train_neural_network(X_train, y_train, epochs=10)
plot_training_history(history)
save_nn(nn_model)
