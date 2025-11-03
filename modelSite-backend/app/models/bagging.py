# models/bagging_regression_model.py
import numpy as np
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from app.utils.data_utils import load_dataset, prepare_features, train_test_split_data, parse_metrics


def process_bagging_regression(file: bytes, filename: str, target_column: str, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, _ = prepare_features(df, target_column)

    if not np.issubdtype(y.dtype, np.number) or y.nunique() <= 10:
        return {"error": "Target appears categorical — use Bagging Classification model instead."}

    valid_metrics = {"r2_score", "mse", "rmse"}
    metrics_list = parse_metrics(metrics_list, valid_metrics)

    X_train, X_test, y_train, y_test = train_test_split_data(X_scaled, y)

    base_model = LinearRegression()
    model = BaggingRegressor(estimator=base_model, n_estimators=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {}
    if "r2_score" in metrics_list:
        results["r2_score"] = round(r2_score(y_test, y_pred), 4)
    if "mse" in metrics_list:
        results["mse"] = round(mean_squared_error(y_test, y_pred), 4)
    if "rmse" in metrics_list:
        results["rmse"] = round(np.sqrt(mean_squared_error(y_test, y_pred)), 4)

    return {
        "model_type": "Bagging Regression",
        "parameters": {"n_estimators": 10, "scaler": "StandardScaler", "random_state": 42},
        "metrics": results,
        "predictions_preview": [{"actual": float(a), "predicted": float(p)} for a, p in zip(y_test[:10], y_pred[:10])]
    }
