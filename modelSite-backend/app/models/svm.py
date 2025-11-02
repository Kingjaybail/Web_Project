import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def process_svm_regression(file: bytes, filename: str, target_column: str):
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

    df[target_column] = pd.to_numeric(df[target_column], errors="coerce")
    df = df.dropna(subset=[target_column])

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X = pd.get_dummies(X, drop_first=True)
    X = X.select_dtypes(include=[np.number])

    if X.empty or y.empty:
        return {"error": "Invalid feature or target data."}

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = SVR(kernel="rbf", C=1.0, epsilon=0.1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n--- SVM Regression: Predictions Preview ---")
    for a, p in zip(y_test[:10], y_pred[:10]):
        print(f"Actual: {a:.4f} | Predicted: {p:.4f}")
    print("-------------------------------------------\n")

    return {
        "model_type": "Support Vector Machine (SVM)",
        "metrics": {"r2_score": round(float(r2), 4),
                    "mse": round(float(mse), 4),
                    "rmse": round(float(rmse), 4)},
        "parameters": {"kernel": "rbf", "C": 1.0, "epsilon": 0.1},
        "predictions_preview": [
            {"actual": float(a), "predicted": float(p)}
            for a, p in zip(y_test[:10], y_pred[:10])
        ],
    }
