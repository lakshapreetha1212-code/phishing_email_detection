from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from features import EmailFeatures

ROOT = Path(__file__).resolve().parent
data = pd.read_csv(ROOT / "emails.csv")
X = data["text"].fillna("").astype(str)
y = data["label"].astype(str)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = Pipeline([
    ("features", FeatureUnion([
        ("text", TfidfVectorizer(ngram_range=(1, 2), max_features=5000, sublinear_tf=True)),
        ("email", EmailFeatures()),
    ])),
    ("classifier", __import__("sklearn").linear_model.LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=42
    )),
])
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\\nMODEL EVALUATION")
print("----------------")
print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")
print("\\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))
print("Confusion matrix (labels: phishing, safe):")
print(confusion_matrix(y_test, predictions, labels=["phishing", "safe"]))

joblib.dump(model, ROOT / "phishing_model.joblib")
print(f"\\nSaved model to: {ROOT / 'phishing_model.joblib'}")
print("Note: this is a learning/demo dataset. Add more diverse labelled emails for meaningful evaluation.")
