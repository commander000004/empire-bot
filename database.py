# database.py

import sqlite3
import random
import json

DB = "empire.db"


def connect():
    return sqlite3.connect(DB)


def init_db():

    db = connect()
    cur = db.cursor()

    # ===== Users =====

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        bale_id TEXT PRIMARY KEY,

        name TEXT,

        coin INTEGER,

        gem INTEGER,

        level INTEGER,

        xp INTEGER,

        last_work INTEGER,

        bank INTEGER,

        card TEXT,

        inventory TEXT,

        job TEXT,

        work_count INTEGER,

        banned INTEGER DEFAULT 0

    )
    """)

    # ===== Groups =====

    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups(

        chat_id TEXT PRIMARY KEY,

        title TEXT

    )
    """)

    db.commit()
    db.close()


# ================= USERS =================


def row_to_user(row):

    if not row:
        return None

    return {

        "bale_id": row[0],
        "name": row[1],

        "coin": row[2],
        "gem": row[3],

        "level": row[4],
        "xp": row[5],

        "last_work": row[6],

        "bank": row[7],

        "card": row[8],

        "inventory": json.loads(row[9]),

        "job": row[10],

        "work_count": row[11],

        "banned": bool(row[12])

    }


def get_user(bale_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM users WHERE bale_id=?",
        (bale_id,)
    )

    row = cur.fetchone()

    db.close()

    return row_to_user(row)


def get_all_users():

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM users"
    )

    rows = cur.fetchall()

    db.close()

    return [
        row_to_user(row)
        for row in rows
    ]


def create_user(
    bale_id,
    name
):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO users
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            bale_id,
            name,

            1000,
            5,

            1,
            0,

            0,

            0,

            None,

            json.dumps([]),

            None,

            0,

            0
        )
    )

    db.commit()
    db.close()


def update_user(user):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE users SET

        name=?,
        coin=?,
        gem=?,
        level=?,
        xp=?,
        last_work=?,
        bank=?,
        card=?,
        inventory=?,
        job=?,
        work_count=?,
        banned=?

        WHERE bale_id=?

        """,
        (

            user["name"],

            user["coin"],

            user["gem"],

            user["level"],

            user["xp"],

            user["last_work"],

            user["bank"],

            user["card"],

            json.dumps(
                user["inventory"],
                ensure_ascii=False
            ),

            user["job"],

            user["work_count"],

            int(user["banned"]),

            user["bale_id"]

        )
    )

    db.commit()
    db.close()


# ================= GROUPS =================


def add_group(
    chat_id,
    title
):

    db = connect()
    cur = db.cursor()

    cur.execute(

        """
        INSERT OR IGNORE
        INTO groups
        VALUES(?,?)
        """,

        (
            str(chat_id),
            title
        )

    )

    db.commit()
    db.close()


def get_all_groups():

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM groups"
    )

    groups = cur.fetchall()

    db.close()

    return groups


# ================= STATS =================


def total_players():

    return len(
        get_all_users()
    )


def total_groups():

    return len(
        get_all_groups()
    )


def total_banned():

    return len(

        [

            u

            for u in get_all_users()

            if u["banned"]

        ]

    )


# ================= CARD =================


def create_card():

    return "EMP-" + str(

        random.randint(

            100000,
            999999

        )

    )
    
    # ================= ADMIN TOOLS =================


def set_user_value(
    bale_id,
    field,
    value
):

    allowed = [
        "coin",
        "gem",
        "xp",
        "level"
    ]


    if field not in allowed:

        return False


    db = connect()

    cur = db.cursor()


    cur.execute(

        f"""
        UPDATE users
        SET {field}=?
        WHERE bale_id=?
        """,

        (
            value,
            str(bale_id)
        )

    )


    changed = cur.rowcount


    db.commit()

    db.close()


    return changed > 0
    # ================= BAN SYSTEM =================


def set_ban(
    bale_id,
    status
):

    db = connect()

    cur = db.cursor()


    cur.execute(
        """
        UPDATE users
        SET banned=?
        WHERE bale_id=?
        """,
        (
            int(status),
            str(bale_id)
        )
    )


    changed = cur.rowcount


    db.commit()

    db.close()


    return changed > 0