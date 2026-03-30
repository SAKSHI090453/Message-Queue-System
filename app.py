import streamlit as st
import pandas as pd
import threading
from db import init_db, get_connection
from producer import produce_message
from utils import run_all

import random

st.subheader("Bulk Message Generator")

if st.button("Generate 100 Messages"):
    for i in range(1, 101):
        message = f"order#{i}"
        priority = random.choice([1, 2, 3])  # random priority

        produce_message(message, priority)

    st.success("✅ 100 messages generated!")
    st.rerun()




# INIT
init_db()

st.title("Message Queue Dashboard")

# PRODUCER INPUT
st.subheader("Send Message")

message = st.text_input("Enter message")

priority = st.selectbox(
    "Priority",
    [1, 2, 3],
    format_func=lambda x: {1: "High", 2: "Medium", 3: "Low"}[x]
)

if st.button("Send"):
    if message:
        produce_message(message, priority)
        st.success("Message added!")
        st.rerun()
        
# CONSUMER CONTROLS
from consumer import consume_one

st.subheader("Queue Controls")


if "processing" not in st.session_state:
    st.session_state.processing = False


if st.button("▶Start Processing All"):
    st.session_state.processing = True


if st.session_state.processing:
    from consumer import consume_one

    processed_count = 0

   
    for _ in range(20):   
        result = consume_one()

        if not result:
            break

        processed_count += 1

    if processed_count > 0:
        st.rerun()
    else:
        st.session_state.processing = False
        st.success("✅ All messages processed")
# ==========================
# DISPLAY TABLES
# ==========================
conn = get_connection()

# Producer Table
st.subheader("Producer Table")
producer_df = pd.read_sql("SELECT * FROM producer", conn)
st.dataframe(producer_df)

# Queue Table 
st.subheader("Queue Table")
queue_df = pd.read_sql("""
SELECT * FROM queue
ORDER BY priority ASC, id ASC
""", conn)

queue_df = pd.read_sql("""
SELECT * FROM queue
ORDER BY priority ASC, id ASC
""", conn)

queue_df["priority"] = queue_df["priority"].map({
    1: "High",
    2: "Medium",
    3: "Low"
})

st.dataframe(queue_df)


# DLQ Table
st.subheader("Dead Letter Queue")
dlq_df = pd.read_sql("SELECT * FROM dlq", conn)
st.dataframe(dlq_df)

conn.close()