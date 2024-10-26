import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(file_path):
    # Load data from CSV
    data = pd.read_csv(file_path)

    # Feature Engineering: Calculate odds difference
    data['odds_diff'] = data['team_1_odds'] - data['team_2_odds']

    # Extract target variable and drop unnecessary columns
    y = data['result']
    X = data.drop(columns=['result', 'team_1_points', 'team_2_points'], errors='ignore')

    # One-hot encoding for categorical variables
    X_encoded = pd.get_dummies(X, columns=['team_1', 'team_2'])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


def preprocess_new_data(team_1, team_2, team_1_odds, team_2_odds):
    """Preprocess data for a single match (e.g., Griffins vs Avalanche)"""
    # Create a dataframe for the new match
    new_data = pd.DataFrame({
        'team_1': [team_1],
        'team_2': [team_2],
        'team_1_odds': [team_1_odds],
        'team_2_odds': [team_2_odds]
    })
    
    # Feature Engineering: calculate the odds difference
    new_data['odds_diff'] = new_data['team_1_odds'] - new_data['team_2_odds']

    # Load the original dataset to ensure consistent encoding
    original_data = pd.read_csv('data/sports_data.csv')

    # Drop unnecessary columns
    original_data = original_data.drop(columns=['result', 'team_1_points', 'team_2_points'], errors='ignore')
    
    # Calculate odds_diff for original data (if not already calculated during training)
    original_data['odds_diff'] = original_data['team_1_odds'] - original_data['team_2_odds']
    
    # Combine the data for consistent encoding
    combined_data = pd.concat([
        original_data[['team_1', 'team_2', 'odds_diff']],
        new_data[['team_1', 'team_2', 'odds_diff']]
    ], axis=0)

    # One-hot encoding
    combined_encoded = pd.get_dummies(combined_data, columns=['team_1', 'team_2'])

    # Select only the new match (last row) with the correct columns
    new_encoded_match = combined_encoded.tail(1).reset_index(drop=True)

    # Ensure all columns that were in the training data are present
    final_features = pd.get_dummies(original_data, columns=['team_1', 'team_2']).columns
    for col in final_features:
        if col not in new_encoded_match.columns:
            new_encoded_match[col] = 0

    # Reorder columns to match training data
    new_encoded_match = new_encoded_match[final_features]

    return new_encoded_match
