# models/deep_neural_network_model.py
import io
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
    confusion_matrix,
)
from app.utils.data_utils import load_dataset, prepare_features, parse_metrics


# ------------------------------
# Dynamic Custom Neural Network
# ------------------------------
class CustomNet(nn.Module):
    def __init__(self, input_size, layers_config):
        super(CustomNet, self).__init__()
        layers = []
        in_features = input_size

        # Build layers dynamically from config
        for layer in layers_config:
            layers.append(nn.Linear(in_features, layer["units"]))
            activation = layer.get("activation", "relu").lower()

            if activation == "relu":
                layers.append(nn.ReLU())
            elif activation == "sigmoid":
                layers.append(nn.Sigmoid())
            elif activation == "tanh":
                layers.append(nn.Tanh())

            in_features = layer["units"]

        # Output layer (1 unit)
        layers.append(nn.Linear(in_features, 1))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


# ------------------------------
# Model Processing Function
# ------------------------------
def process_deep_neural_network(file: bytes, filename: str, target_column: str, model_config, metrics_list=None):
    df = load_dataset(file, filename)
    X_scaled, y, feature_names = prepare_features(df, target_column)

    # Accept either JSON string or already parsed dict
    if isinstance(model_config, str):
        try:
            config = json.loads(model_config)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON for model_config"}
    else:
        config = model_config or {}

    # Extract hyperparameters
    layers_config = config.get("layers", [{"units": 32, "activation": "relu"}])
    learning_rate = config.get("learning_rate", 0.001)
    epochs = config.get("epochs", 50)
    batch_size = config.get("batch_size", 16)
    problem_type = config.get("problem_type", "regression").lower()

    metrics_list = parse_metrics(metrics_list, {"mse", "r2", "accuracy", "f1_score", "confusion_matrix"})

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Convert to tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(
        y_train.values if hasattr(y_train, "values") else y_train,
        dtype=torch.float32,
    ).view(-1, 1)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test_np = y_test.values if hasattr(y_test, "values") else y_test

    # Build model
    model = CustomNet(X_train.shape[1], layers_config)
    print("\n Custom Neural Network Architecture:")
    print(model, "\n")

    criterion = nn.MSELoss() if problem_type == "regression" else nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)


    epoch_losses = []  # ✅ record loss per epoch

    model.train()
    for epoch in range(epochs):
        batch_losses = []
        for i in range(0, len(X_train), batch_size):
            X_batch = X_train[i : i + batch_size]
            y_batch = y_train[i : i + batch_size]

            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            batch_losses.append(loss.item())

        avg_epoch_loss = float(np.mean(batch_losses))
        epoch_losses.append({"epoch": epoch + 1, "loss": avg_epoch_loss})
        if epoch % max(1, epochs // 5) == 0:
            print(f"Epoch [{epoch+1}/{epochs}] - Loss: {avg_epoch_loss:.4f}")

    model.eval()
    with torch.no_grad():
        preds = model(X_test).numpy().flatten()

    results = {}
    if problem_type == "regression":
        results["mse"] = round(mean_squared_error(y_test_np, preds), 4)
        results["r2_score"] = round(r2_score(y_test_np, preds), 4)
    else:
        preds_binary = (preds > 0.5).astype(int)
        results["accuracy"] = round(accuracy_score(y_test_np, preds_binary), 4)
        results["f1_score"] = round(f1_score(y_test_np, preds_binary, average="weighted"), 4)
        results["confusion_matrix"] = confusion_matrix(y_test_np, preds_binary).tolist()

    return {
        "model_type": "Custom Deep Neural Network",
        "config_used": config,
        "metrics": results,
        "training_loss": epoch_losses,
        "predictions_preview": [
            {"actual": float(a), "predicted": float(p)}
            for a, p in zip(y_test_np[:10], preds[:10])
        ],
    }
