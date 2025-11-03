# models/linear_regression_model.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from app.utils.data_utils import load_dataset, prepare_features, train_test_split_data, parse_metrics


def process_linear_regression(file: bytes, filename: str, target_column: str, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, feature_names = prepare_features(df, target_column)

    # --- Validate target ---
    if not np.issubdtype(y.dtype, np.number):
        return {"error": "Target column is not numeric. Use a classification model instead."}
    if y.nunique() <= 10:
        return {"error": "Target appears categorical. Use classification model instead."}

    valid_metrics = {"mse", "mae", "r2"}
    metrics_list = parse_metrics(metrics_list, valid_metrics)

    X_train, X_test, y_train, y_test = train_test_split_data(X_scaled, y)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {}
    if "mse" in metrics_list:
        results["mse"] = round(mean_squared_error(y_test, y_pred), 4)
    if "mae" in metrics_list:
        results["mae"] = round(mean_absolute_error(y_test, y_pred), 4)
    if "r2" in metrics_list:
        results["r2_score"] = round(r2_score(y_test, y_pred), 4)

    return {
        "model_type": "Linear Regression",
        "metrics": results,
        "coefficients": dict(zip(feature_names, np.round(model.coef_, 4))),
        "intercept": round(float(model.intercept_), 4),
        "predictions_preview": [{"actual": float(a), "predicted": float(p)} for a, p in zip(y_test[:10], y_pred[:10])]
    }
