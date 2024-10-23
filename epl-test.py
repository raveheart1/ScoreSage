import pandas as pd
from catboost import CatBoostClassifier, Pool, cv
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv('/Users/gordon/Projects/ScoreSage/data/premier-league-matches.csv')

# Step 1: Preprocessing the target variable (FTR)
df['FTR'] = df['FTR'].map({'H': 0, 'A': 1, 'D': 2})

# Step 2: Select features and target
X = df[['Season_End_Year', 'Home', 'Away', 'HomeGoals', 'AwayGoals']]
y = df['FTR']

# Step 3: Prepare the data pool with categorical features for CatBoost
train_pool = Pool(X, y, cat_features=['Home', 'Away'])

# Step 4: Set cross-validation parameters for CatBoost
cv_params = {
    'iterations': 500,
    'depth': 6,
    'learning_rate': 0.1,
    'loss_function': 'MultiClass'
}

# Step 5: Perform cross-validation using CatBoost's cv function
cv_results = cv(train_pool, cv_params, fold_count=5, verbose=True)

# Step 6: Get the mean accuracy from the cross-validation results
mean_accuracy = cv_results['test-MultiClass-accuracy-mean'].max()
print(f"Mean cross-validation accuracy: {mean_accuracy:.2f}")

# Step 7: Train the CatBoostClassifier on the full training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = CatBoostClassifier(iterations=500, depth=6, learning_rate=0.1, loss_function='MultiClass')

# Train the model
model.fit(X_train, y_train, cat_features=['Home', 'Away'], verbose=100)

# Step 8: Make predictions and evaluate the model on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Set Accuracy: {accuracy:.2f}")
