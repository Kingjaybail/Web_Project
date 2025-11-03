# models/logistic_regression_model.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.utils.data_utils import load_dataset, prepare_features, train_test_split_data, parse_metrics
import pandas as pd


def process_logistic_regression(file: bytes, filename: str, target_column: str, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, feature_names = prepare_features(df, target_column)

    # --- Validate target ---
    if not y.dtype == object and y.nunique() > 10:
        return {"error": "Target appears continuous. Use a regression model instead."}

    # Factorize categorical labels
    y = pd.factorize(y)[0]

    # --- Metrics list ---
    valid_metrics = {"accuracy", "precision", "recall", "f1_score", "confusion_matrix"}
    metrics_list = parse_metrics(metrics_list, valid_metrics)

    # --- Train/Test Split ---
    X_train, X_test, y_train, y_test = train_test_split_data(X_scaled, y)

    # --- Train Model ---
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # --- Metrics ---
    results = {}
    if "accuracy" in metrics_list:
        results["accuracy"] = round(accuracy_score(y_test, y_pred), 4)
    if "precision" in metrics_list:
        results["precision"] = round(precision_score(y_test, y_pred, average="weighted", zero_division=0), 4)
    if "recall" in metrics_list:
        results["recall"] = round(recall_score(y_test, y_pred, average="weighted", zero_division=0), 4)
    if "f1_score" in metrics_list:
        results["f1_score"] = round(f1_score(y_test, y_pred, average="weighted", zero_division=0), 4)
    if "confusion_matrix" in metrics_list:
        results["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()

    return {
        "model_type": "Logistic Regression",
        "metrics": results,
        "coefficients": dict(zip(feature_names, np.round(model.coef_[0], 4))),
        "intercept": round(float(model.intercept_[0]), 4),
        "predictions_preview": [{"actual": int(a), "predicted": int(p)} for a, p in zip(y_test[:10], y_pred[:10])]
    }



