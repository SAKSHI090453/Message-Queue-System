from db import get_connection

def produce_message(message, priority):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert into producer table
    cursor.execute("""
    INSERT INTO producer (message, priority)
    VALUES (?, ?)
    """, (message, priority))

    # Insert into queue table
    cursor.execute("""
    INSERT INTO queue (message, priority, retry_count, status)
    VALUES (?, ?, 0, 'pending')
    """, (message, priority))

    conn.commit()
    conn.close()