# Message-Queue-System
A lightweight Message Queue System built using Python, SQLite, and Streamlit, demonstrating core concepts of distributed systems such as priority-based processing, retries, fault tolerance, and Dead Letter Queue (DLQ).

**Features**
1.Priority-based Processing
   High (1) → Medium (2) → Low (3)
   FIFO ordering within same priority
2.Retry Mechanism
   Messages are retried on failure
   Configurable retry count
3.Dead Letter Queue (DLQ)
   Messages exceeding retry limit are moved to DLQ
   Prevents blocking of queue
4.Acknowledgment System
   Messages marked as completed after successful processing
5.Persistent Storage
   SQLite ensures no message loss
6.Interactive Dashboard
   Built using Streamlit
   View producer, queue, and DLQ in real-time

**Tech Stack**
  **-**Python
  **-**SQLite
  **-**Streamlit
  **-**Pandas

