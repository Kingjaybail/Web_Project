import io
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json

def load_dataset(file: bytes, filename: str) -> pd.DataFrame:
    ext = filename.split(".")[-1].lower()
    if ext == "csv":
        return pd.read_csv(io.BytesIO(file))
    elif ext in ["xls", "xlsx"]:
        return pd.read_excel(io.BytesIO(file))
    elif ext == "txt":
        return pd.read_csv(io.BytesIO(file), delimiter="\t")
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def prepare_features(df: pd.DataFrame, target_column: str):
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    df = df.dropna(subset=[target_column])
    X = df.drop(columns=[target_column])
    y = df[target_column]

    X = pd.get_dummies(X, drop_first=True).select_dtypes(include=[np.number])
    if X.empty:
        raise ValueError("No valid numeric features found.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns

def parse_metrics(metrics_list, valid_metrics):
    if isinstance(metrics_list, str):
        try:
            metrics_list = json.loads(metrics_list)
        except json.JSONDecodeError:
            metrics_list = []
    elif metrics_list is None:
        metrics_list = []
    metrics_list = [m.lower().replace(" ", "_") for m in metrics_list]
    return [m for m in metrics_list if m in valid_metrics] or list(valid_metrics)


def train_test_split_data(X_scaled, y):
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
