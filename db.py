import sqlite3

DB_NAME = "queue.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Producer Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        priority INTEGER
    )
    """)

    # Queue Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        priority INTEGER,
        retry_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending'
    )
    """)

    # DLQ Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dlq (
        id INTEGER,
        message TEXT,
        priority INTEGER,
        retry_count INTEGER
    )
    """)

    conn.commit()
    conn.close()