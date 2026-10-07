# from fastapi import FastAPI,status,HTTPException,Depends,Request,Header
import sqlite3

from fastapi import FastAPI,Request
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "test.db"

conn = sqlite3.connect(DB_PATH,check_same_thread=False)

cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS todos(
id INTEGER PRIMARY KEY,
title TEXT,
completed TEXT)""")

conn.commit()

cursor.execute("PRAGMA table_info(todos)")
print(cursor.fetchall())

@app.get("/user")
def home():
    return {
        "messages":"Database Connected"
    }