import io
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

def process_linear_regression(file: bytes, filename: str, target_column: str, metrics_list=None):
    ext = filename.split(".")[-1].lower()
    if ext == "csv":
        df = pd.read_csv(io.BytesIO(file))
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(io.BytesIO(file))
    elif ext == "txt":
        df = pd.read_csv(io.BytesIO(file), delimiter="\t")
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    if target_column not in df.columns:
        return {"error": f"Target column '{target_column}' not found in dataset."}

    if isinstance(metrics_list, str):
        try:
            metrics_list = json.loads(metrics_list)
        except json.JSONDecodeError:
            metrics_list = []
    elif metrics_list is None:
        metrics_list = []

    metrics_list = [m.lower().replace(" ", "_") for m in metrics_list]
    is_numeric_target = pd.api.types.is_numeric_dtype(df[target_column])
    model_type = "regression" if is_numeric_target else "classification"
    valid_metrics = {"r2_score", "mse", "rmse"} if model_type == "regression" else {"accuracy", "precision", "recall", "f1_score", "confusion_matrix"}
    metrics_list = [m for m in metrics_list if m in valid_metrics] or list(valid_metrics)

    df = df.dropna(subset=[target_column])
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X = pd.get_dummies(X, drop_first=True).select_dtypes(include=[np.number])
    if X.empty or y.empty:
        return {"error": "No valid numeric features found."}

    X_scaled = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = LinearRegression() if model_type == "regression" else LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {}
    if model_type == "regression":
        if "r2_score" in metrics_list: results["r2_score"] = round(r2_score(y_test, y_pred), 4)
        if "mse" in metrics_list: results["mse"] = round(mean_squared_error(y_test, y_pred), 4)
        if "rmse" in metrics_list: results["rmse"] = round(np.sqrt(mean_squared_error(y_test, y_pred)), 4)
    else:
        if "accuracy" in metrics_list: results["accuracy"] = round(accuracy_score(y_test, y_pred), 4)
        if "precision" in metrics_list: results["precision"] = round(precision_score(y_test, y_pred, average="weighted"), 4)
        if "recall" in metrics_list: results["recall"] = round(recall_score(y_test, y_pred, average="weighted"), 4)
        if "f1_score" in metrics_list: results["f1_score"] = round(f1_score(y_test, y_pred, average="weighted"), 4)
        if "confusion_matrix" in metrics_list: results["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()

    return {
        "model_type": "Linear Regression" if model_type == "regression" else "Logistic Regression",
        "metrics": results,
        "coefficients": dict(zip(X.columns, np.round(model.coef_, 4))) if hasattr(model, "coef_") else None,
        "intercept": round(float(model.intercept_), 4) if hasattr(model, "intercept_") else None,
        "predictions_preview": [{"actual": float(a), "predicted": float(p)} for a, p in zip(y_test[:10], y_pred[:10])],
    }
