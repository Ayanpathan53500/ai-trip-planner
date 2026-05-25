# import sqlite3

# DB_NAME = "memory/chat_memory.db"

# # Create table
# def init_db():

#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS chats (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_message TEXT,
#         bot_response TEXT
#     )
#     ''')

#     conn.commit()
#     conn.close()


# # Save messages
# def save_chat(user_msg, bot_msg):

#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO chats (user_message, bot_response) VALUES (?, ?)",
#         (user_msg, bot_msg)
#     )

#     conn.commit()
#     conn.close()


# # Load chat history
# def load_chats():

#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM chats")

#     data = cursor.fetchall()

#     conn.close()

#     return data



# if __name__ == "__main__":
#     init_db()
#     print("Database created successfully")


import sqlite3
import os

# Create memory folder automatically
os.makedirs("memory", exist_ok=True)

DB_NAME = "memory/chat_memory.db"

# Create table
def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT
    )
    ''')

    conn.commit()
    conn.close()


# Save messages
def save_chat(user_msg, bot_msg):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (user_message, bot_response) VALUES (?, ?)",
        (user_msg, bot_msg)
    )

    conn.commit()
    conn.close()


# Load chats
def load_chats():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chats")

    data = cursor.fetchall()

    conn.close()

    return data


def clear_session(session_id: str = "default"):
    """Delete all messages for a session."""
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute("DELETE FROM chats WHERE session_id = ?", (session_id,))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database created successfully")