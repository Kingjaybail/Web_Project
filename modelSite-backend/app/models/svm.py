# models/svm_regression_model.py
import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from app.utils.data_utils import load_dataset, prepare_features, train_test_split_data, parse_metrics


def process_svm_model(file: bytes, filename: str, target_column: str, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, _ = prepare_features(df, target_column)

    if not np.issubdtype(y.dtype, np.number) or y.nunique() <= 10:
        return {"error": "Target appears categorical — use SVM Classification model instead."}

    valid_metrics = {"r2_score", "mse", "rmse"}
    metrics_list = parse_metrics(metrics_list, valid_metrics)

    X_train, X_test, y_train, y_test = train_test_split_data(X_scaled, y)
    model = SVR(kernel="rbf", C=1.0, epsilon=0.1)
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
        "model_type": "SVM Regression",
        "parameters": {"kernel": "rbf", "C": 1.0, "epsilon": 0.1, "scaler": "StandardScaler"},
        "metrics": results,
        "predictions_preview": [{"actual": float(a), "predicted": float(p)} for a, p in zip(y_test[:10], y_pred[:10])]
    }
