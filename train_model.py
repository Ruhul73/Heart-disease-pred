import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def main():
    df = pd.read_csv("heart.csv")
    if 'target' not in df.columns:
        raise SystemExit("'target' column not found in heart.csv")

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    print('Training model...')
    pipe.fit(X_train, y_train)

    train_acc = pipe.score(X_train, y_train)
    test_acc = pipe.score(X_test, y_test)
    print(f'Train accuracy: {train_acc:.4f}')
    print(f'Test accuracy: {test_acc:.4f}')

    model_path = 'heart_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)

    print(f'Model saved to {model_path}')

if __name__ == '__main__':
    main()
