# models/random_forest_model.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from app.utils.data_utils import load_dataset, prepare_features, train_test_split_data, parse_metrics


def process_random_forest(file: bytes, filename: str, target_column: str, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, feature_names = prepare_features(df, target_column)

    # --- Detect problem type ---
    if np.issubdtype(y.dtype, np.number) and y.nunique() > 10:
        problem_type = "regression"
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        valid_metrics = {"mse", "mae", "r2"}
    else:
        problem_type = "classification"
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        valid_metrics = {"accuracy", "precision", "recall", "f1_score", "confusion_matrix"}
        # Encode non-numeric target if necessary
        if not np.issubdtype(y.dtype, np.number):
            from pandas import factorize
            y = factorize(y)[0]

    # --- Parse requested metrics ---
    metrics_list = parse_metrics(metrics_list, valid_metrics)

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split_data(X_scaled, y)

    # --- Train model ---
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # --- Compute metrics ---
    results = {}
    if problem_type == "regression":
        if "mse" in metrics_list:
            results["mse"] = round(mean_squared_error(y_test, y_pred), 4)
        if "mae" in metrics_list:
            results["mae"] = round(mean_absolute_error(y_test, y_pred), 4)
        if "r2" in metrics_list:
            results["r2_score"] = round(r2_score(y_test, y_pred), 4)
    else:
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

    # --- Feature importances ---
    feature_importances = dict(zip(feature_names, np.round(model.feature_importances_, 4)))

    # --- Return consistent response ---
    return {
        "model_type": "Random Forest (Regression)" if problem_type == "regression" else "Random Forest (Classification)",
        "metrics": results,
        "feature_importances": feature_importances,
        "parameters": {
            "n_estimators": model.n_estimators,
            "max_depth": model.max_depth,
            "random_state": 42,
            "n_jobs": -1
        },
        "predictions_preview": [
            {"actual": float(a), "predicted": float(p)} for a, p in zip(y_test[:10], y_pred[:10])
        ],
    }
