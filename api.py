from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import math
import sqlite3

from auth import hash_password, verify_password, create_token
from database import init_db, get_connection

import os

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- INIT DB ----------------
init_db()

# ---------------- TOKEN VERIFY ----------------
def verify_token(token: str):
    try:
        from jose import jwt

        SECRET_KEY = "mysecretkey123"

        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded

    except:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "API working"}


# ---------------- REGISTER ----------------
@app.post("/register")
def register(username: str = Query(...), password: str = Query(...)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hash_password(password))
    )

    conn.commit()
    conn.close()

    return {"message": "User created"}


# ---------------- LOGIN ----------------
@app.post("/login")
def login(
    username: str = Query(...),
    password: str = Query(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        stored_password = user[0]   # ✅ FIXED HERE

        if not verify_password(password, stored_password):
            raise HTTPException(status_code=401, detail="Wrong password")

        token = create_token({"user": username})

        return {
            "message": "Login success",
            "token": token
        }

    finally:
        conn.close()


# ---------------- DESIGN ----------------
@app.get("/design")
def design(kva: float, hv: float, lv: float, frequency: float, token: str):

    user_data = verify_token(token)
    username = user_data["user"]

    hv_current = (kva * 1000) / (math.sqrt(3) * hv)
    lv_current = (kva * 1000) / (math.sqrt(3) * lv)

    core_area = 1.152 * math.sqrt(kva)

    B = 1.2
    tpv = 1 / (4.44 * frequency * B * (core_area / 10000))

    hv_turns = tpv * hv
    lv_turns = tpv * lv

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO designs (
            username, kva, hv, lv, frequency,
            hv_current, lv_current, core_area
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username, kva, hv, lv, frequency,
        hv_current, lv_current, core_area
    ))

    conn.commit()
    conn.close()

    return {
        "kva": kva,
        "hv_current": hv_current,
        "lv_current": lv_current,
        "core_area": core_area,
        "hv_turns": hv_turns,
        "lv_turns": lv_turns
    }


# ---------------- HISTORY ----------------
@app.get("/history")
def history(token: str):

    user_data = verify_token(token)
    username = user_data["user"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM designs WHERE username=? ORDER BY id DESC",
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return {"data": [dict(row) for row in rows]}


# ---------------- USERS (DEBUG) ----------------
@app.get("/users")
def users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]