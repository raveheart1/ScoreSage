import pandas as pd
try:
    from catboost import CatBoostClassifier
except ModuleNotFoundError:
    !pip install catboost
    from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = pd.read_csv("/content/premier-league-matches.csv")

data['result'] = data.apply(lambda row: 'win' if row['HomeGoals'] > row['AwayGoals'] else ('lose' if row['HomeGoals'] < row['AwayGoals'] else 'draw'), axis=1)

data = data.drop(columns=['HomeGoals', 'AwayGoals'])

data['home_team'] = data['Home'].astype('category').cat.codes
data['away_team'] = data['Away'].astype('category').cat.codes

data['home_win'] = data['result'].apply(lambda x: 1 if x == 'win' else 0)
data['away_win'] = data['result'].apply(lambda x: 1 if x == 'lose' else 0)

data['home_team_form'] = data.groupby('home_team')['home_win'].transform(
    lambda x: x.shift().rolling(5).sum()
).fillna(0)

data['away_team_form'] = data.groupby('away_team')['away_win'].transform(
    lambda x: x.shift().rolling(5).sum()
).fillna(0)

result_mapping = {'win': 1, 'draw': 0, 'lose': -1}
data['numeric_result'] = data['result'].map(result_mapping)

data['home_team_avg_gd'] = data.groupby('home_team')['numeric_result'].transform(
    lambda x: x.shift().expanding().mean()
).fillna(0)

data['away_team_avg_gd'] = data.groupby('away_team')['numeric_result'].transform(
    lambda x: x.shift().expanding().mean()
).fillna(0)

data['is_home_game'] = 1


data['h2h_record'] = data.apply(
    lambda row: len(data[
        (data['home_team'] == row['home_team']) &
        (data['away_team'] == row['away_team']) &
        (data.index < row.name)
    ]),
    axis=1
)

data = data.drop(columns=['home_win', 'away_win', 'numeric_result'])

y = data['result']

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("Classes in label_encoder:")
print(label_encoder.classes_)
print("Data type of classes:", type(label_encoder.classes_[0]))

print("First few entries of y:")
print(y.head())
print("Data type of y elements:", type(y.iloc[0]))


X = data[['home_team', 'away_team', 'home_team_form', 'away_team_form', 
          'home_team_avg_gd', 'away_team_avg_gd', 'is_home_game', 'h2h_record']]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.1,
    depth=6,
    loss_function='MultiClass',
    eval_metric='Accuracy',
    verbose=100,
    random_seed=42
)

model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    use_best_model=True,
    early_stopping_rounds=50
)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print('Classification Report:')
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()