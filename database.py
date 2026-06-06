import os
import sqlite3

def get_connection():
    import os
    print("DATABASE PATH:", os.path.abspath("app.db"))
    conn = sqlite3.connect("app.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- DESIGN TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS designs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        kva REAL,
        hv REAL,
        lv REAL,
        frequency REAL,
        hv_current REAL,
        lv_current REAL,
        core_area REAL
    )
    """)

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()