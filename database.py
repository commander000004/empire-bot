import sqlite3
import json

from config import (
    START_COIN,
    START_GEM,
    START_LEVEL,
    START_XP,
    START_BANK
)

DATABASE_FILE = "empire.db"


# -------------------------
# DATABASE
# -------------------------

conn = sqlite3.connect(DATABASE_FILE)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()


def create_tables():

    # Users

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        game_id INTEGER UNIQUE,

        bale_id INTEGER UNIQUE,

        name TEXT,

        coin INTEGER,

        gem INTEGER,

        level INTEGER,

        xp INTEGER,

        job TEXT,

        last_work INTEGER

    )
    """)

    # Bank

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank (

        user_id INTEGER PRIMARY KEY,

        balance INTEGER,

        account TEXT,

        card TEXT,

        loan INTEGER,

        loan_time INTEGER,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    # Inventory

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        item TEXT,

        count INTEGER,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    # Crypto

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        coin TEXT,

        amount REAL,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    conn.commit()


create_tables()
