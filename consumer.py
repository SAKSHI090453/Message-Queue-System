import time
import random
from db import get_connection
from config import MAX_RETRIES, FAILURE_RATE, PROCESSING_DELAY


def process_message(message):
    print(f"Processing: {message}")
    time.sleep(PROCESSING_DELAY)

    if random.random() < FAILURE_RATE:
        print("❌ Failed")
        return False

    print("✅ Success")
    return True


def consume_one():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, message, priority, retry_count
    FROM queue
    WHERE status IN ('pending', 'failed')
    ORDER BY priority ASC, id ASC
    LIMIT 1
    """)

    msg = cursor.fetchone()

    if not msg:
        conn.close()
        return False  

    msg_id, message, priority, retry_count = msg

    if retry_count >= MAX_RETRIES:
        cursor.execute("DELETE FROM queue WHERE id=?", (msg_id,))
        cursor.execute("""
        INSERT INTO dlq (id, message, priority, retry_count)
        VALUES (?, ?, ?, ?)
        """, (msg_id, message, priority, retry_count))

        conn.commit()
        conn.close()

        print(f" {message} → DLQ")
        return True

    cursor.execute("UPDATE queue SET status='processing' WHERE id=?", (msg_id,))
    conn.commit()

    success = process_message(message)

    if success:
        cursor.execute("""
        UPDATE queue SET status='completed'
        WHERE id=?
        """, (msg_id,))
    else:
        retry_count += 1
        cursor.execute("""
        UPDATE queue
        SET retry_count=?, status='failed'
        WHERE id=?
        """, (retry_count, msg_id))

    conn.commit()
    conn.close()

    return True