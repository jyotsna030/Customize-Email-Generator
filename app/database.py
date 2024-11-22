import sqlite3

def create_db():
    conn = sqlite3.connect("email_status.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_email_status(statuses):
    conn = sqlite3.connect("email_status.db")
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO email_status (email, status) VALUES (?, ?)",
        [(status["email"], status["status"]) for status in statuses]
    )
    conn.commit()
    conn.close()

import streamlit as st
import websocket
import json

def get_status_updates():
    ws = websocket.create_connection("ws://127.0.0.1:8000/ws/")
    while True:
        message = json.loads(ws.recv())
        yield message

st.subheader("Real-Time Email Status")
status_updates = st.empty()

for update in get_status_updates():
    status_updates.write(update)


def get_email_status():
    conn = sqlite3.connect("email_status.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, status FROM email_status")
    results = cursor.fetchall()
    conn.close()
    return [{"email": row[0], "status": row[1]} for row in results]


