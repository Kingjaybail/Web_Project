import sqlite3
import json
from datetime import datetime

DB_NAME = "app/database/users.db"

def get_connection():
    """Helper to open a new database connection."""
    return sqlite3.connect(DB_NAME)

def initialize_db():
    """Initialize users and model_results tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # Create model_results table (ties metrics to usernames)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            dataset_name TEXT NOT NULL,
            model_type TEXT NOT NULL,
            target_column TEXT,
            metrics TEXT,
            metric_value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized successfully with 'users' and 'model_results' tables.")


# ------------------------------
# User Management
# ------------------------------
def add_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return {"success": "success"}
    except sqlite3.IntegrityError:
        return {"failed": "User already exists"}
    finally:
        conn.close()

def get_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return bool(user)


# ------------------------------
# Model Tracking
# ------------------------------
def save_model_result(username: str, dataset_name: str, model_type: str, target_column: str, metrics: dict):
    conn = get_connection()
    cursor = conn.cursor()

    # Extract a key metric for comparison
    metric_value = metrics.get("accuracy") or metrics.get("r2_score") or (1 / metrics.get("mse", 1))

    cursor.execute("""
        INSERT INTO model_results (username, dataset_name, model_type, target_column, metrics, metric_value, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        dataset_name,
        model_type,
        target_column,
        json.dumps(metrics),
        round(metric_value, 4),
        datetime.now(),
    ))

    conn.commit()
    conn.close()


def get_user_model_history(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dataset_name, model_type, target_column, metrics, metric_value, timestamp
        FROM model_results
        WHERE username = ?
        ORDER BY timestamp DESC
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for dataset, model, target, metrics_json, metric_value, ts in rows:
        try:
            metrics = json.loads(metrics_json)
        except json.JSONDecodeError:
            metrics = {}
        history.append({
            "dataset_name": dataset,
            "model": model,
            "target_column": target,
            "metric_value": metric_value,
            "metrics": metrics,
            "timestamp": ts
        })
    return history


def clear_user_model_history(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM model_results WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# Run on import
initialize_db()
