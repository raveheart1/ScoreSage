import pandas as pd
from catboost import CatBoostClassifier, Pool, cv
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv('premier-league-matches.csv')

df['FTR'] = df['FTR'].map({'H': 0, 'A': 1, 'D': 2})

X = df[['Season_End_Year', 'Home', 'Away', 'HomeGoals', 'AwayGoals']]
y = df['FTR']

train_pool = Pool(X, y, cat_features=['Home', 'Away'])

cv_params = {
    'iterations': 500,
    'depth': 6,
    'learning_rate': 0.1,
    'loss_function': 'MultiClass'
}

cv_results = cv(train_pool, cv_params, fold_count=5, verbose=True)

mean_accuracy = cv_results['test-MultiClass-accuracy-mean'].max()
print(f"Mean cross-validation accuracy: {mean_accuracy:.2f}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = CatBoostClassifier(iterations=500, depth=6, learning_rate=0.1, loss_function='MultiClass')

model.fit(X_train, y_train, cat_features=['Home', 'Away'], verbose=100)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Set Accuracy: {accuracy:.2f}")
