from typing import Tuple, Dict, Any
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def get_iris_data():
    iris = load_iris()
    X = iris.data
    y = iris.target
    return X, y, iris.feature_names, iris.target_names


def build_model(model_name: str) -> Pipeline:
    if model_name == "Random Forest":
        clf = RandomForestClassifier(n_estimators=200, random_state=42)
    else:
        clf = LogisticRegression(max_iter=500)
    pipe = make_pipeline(StandardScaler(), clf)
    return pipe


def train_iris_model(model_name: str = "Logistic Regression", test_size: float = 0.2, random_state: int = 42):
    X, y, feature_names, target_names = get_iris_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    model = build_model(model_name)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=target_names, zero_division=0)
    metrics = {"accuracy": acc, "classification_report": report, "target_names": target_names}
    return model, metrics


def predict_iris(model: Pipeline, features: np.ndarray):
    if features.ndim == 1:
        features = features.reshape(1, -1)
    pred_idx = int(model.predict(features)[0])
    # Extract classes from the final estimator in the pipeline
    final_estimator = model.steps[-1][1]
    classes = final_estimator.classes_
    proba = model.predict_proba(features)[0]
    # Map probabilities to class indices
    label_probs = {int(cls): float(prob) for cls, prob in zip(classes, proba)}
    return pred_idx, label_probs
