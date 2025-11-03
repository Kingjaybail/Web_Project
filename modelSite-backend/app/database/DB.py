import sqlite3
import json
from datetime import datetime

DB_NAME = "app/database/users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # Model results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            dataset_name TEXT NOT NULL,
            model_type TEXT NOT NULL,
            target_column TEXT,
            metrics TEXT,
            metric_value REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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
        return {'success': 'success'}
    except sqlite3.IntegrityError:
        return {'failed': 'failed'}
    finally:
        conn.close()


def delete_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def change_password(username: str, new_password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def get_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return bool(user)


# ------------------------------
# Model History Functions
# ------------------------------

def save_model_result(username: str, dataset_name: str, model_type: str, target_column: str, metrics: dict):
    """Save a model run to the history table."""
    conn = get_connection()
    cursor = conn.cursor()

    # Choose a single numeric value to summarize performance
    metric_value = (
            metrics.get("accuracy")
            or metrics.get("r2_score")
            or (1 / metrics.get("mse", 1))
    )

    cursor.execute("""
        INSERT INTO model_results 
        (username, dataset_name, model_type, target_column, metrics, metric_value, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        dataset_name,
        model_type,
        target_column,
        json.dumps(metrics),
        round(metric_value, 4),
        datetime.now()
    ))

    conn.commit()
    conn.close()


def get_user_model_history(username: str):
    """Return all stored models for a given user."""
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
            "target": target,
            "metric": round(metric_value, 4) if metric_value else None,
            "metrics": metrics,
            "timestamp": ts
        })
    return history


def clear_user_model_history(username: str):
    """Delete all results for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM model_results WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# Initialize DB when this file is imported
initialize_db()
