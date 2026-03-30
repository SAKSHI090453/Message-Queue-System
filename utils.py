import time
from consumer import consume_one
from db import get_connection


def get_remaining_messages():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM queue
    WHERE status != 'completed'
    """)

    count = cursor.fetchone()[0]
    conn.close()

    return count


def run_all():
    while True:
        remaining = get_remaining_messages()

        if remaining == 0:
            print("✅ All messages processed")
            break

        processed = consume_one()

        if not processed:
            print("⏳ Waiting...")
            time.sleep(2)
        else:
            time.sleep(1)