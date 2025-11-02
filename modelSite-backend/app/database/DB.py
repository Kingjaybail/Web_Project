import sqlite3

DB_NAME = "app/database/users.db"

def get_connection():
    """Helper to open a new database connection."""
    return sqlite3.connect(DB_NAME)


def add_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    print(username, password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return {'success': 'success'}
    except sqlite3.IntegrityError:
        return {'failed': 'failed'}
    finally:
        conn.close()


def delete_user(username: str):
    """Deletes a user by username. Returns True if deleted, False if not found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def change_password(username: str, new_password: str):
    """Updates the user's password. Returns True if successful, False if user not found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def get_user(username: str, password: str):
    """Returns user info if username and password match, otherwise None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True
    return False

