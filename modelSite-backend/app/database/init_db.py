import sqlite3

DB_NAME = "users.db"

def get_connection():
    """Helper to open a new database connection."""
    return sqlite3.connect(DB_NAME)


def initialize_db():
    """Initializes the SQLite3 database and creates the users table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized successfully with 'users' table.")
    
    
initialize_db()