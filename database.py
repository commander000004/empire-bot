import sqlite3
import time

from config import (
    START_COIN,
    START_GEM,
    START_LEVEL,
    START_XP,
    START_BANK
)


# ==================================================
# DATABASE
# ==================================================

DATABASE_NAME = "empire.db"


conn = sqlite3.connect(DATABASE_NAME)

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


# ==================================================
# CREATE TABLES
# ==================================================

def create_tables():

    # ---------------- USERS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        game_id INTEGER UNIQUE NOT NULL,

        bale_id INTEGER UNIQUE NOT NULL,

        name TEXT NOT NULL,

        coin INTEGER NOT NULL DEFAULT 0,

        gem INTEGER NOT NULL DEFAULT 0,

        level INTEGER NOT NULL DEFAULT 1,

        xp INTEGER NOT NULL DEFAULT 0,

        job TEXT,

        last_work INTEGER NOT NULL DEFAULT 0

    )
    """)

    # ---------------- BANK ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank (

        user_id INTEGER PRIMARY KEY,

        balance INTEGER NOT NULL DEFAULT 0,

        account TEXT UNIQUE,

        card TEXT UNIQUE,

        loan INTEGER NOT NULL DEFAULT 0,

        loan_time INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- INVENTORY ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        item TEXT NOT NULL,

        count INTEGER NOT NULL DEFAULT 1,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- CRYPTO ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        symbol TEXT NOT NULL,

        amount REAL NOT NULL DEFAULT 0,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- TRANSACTIONS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        sender_id INTEGER,

        receiver_id INTEGER,

        amount INTEGER NOT NULL,

        tax INTEGER NOT NULL DEFAULT 0,

        type TEXT NOT NULL,

        created_at INTEGER NOT NULL,

        FOREIGN KEY(sender_id)
            REFERENCES users(id)
            ON DELETE SET NULL,

        FOREIGN KEY(receiver_id)
            REFERENCES users(id)
            ON DELETE SET NULL

    )
    """)

    # ---------------- ADMIN LOGS ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        admin_id INTEGER NOT NULL,

        action TEXT NOT NULL,

        target_id INTEGER,

        amount INTEGER,

        created_at INTEGER NOT NULL,

        FOREIGN KEY(admin_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    conn.commit()


create_tables()
# ==================================================
# USER HELPERS
# ==================================================

def row_to_user(row):

    if row is None:
        return None

    user = dict(row)

    # ---------------- BANK ----------------

    cursor.execute(
        """
        SELECT
            balance,
            account,
            card,
            loan,
            loan_time
        FROM bank
        WHERE user_id = ?
        """,
        (user["id"],)
    )

    bank = cursor.fetchone()

    if bank:

        user["bank"] = {

            "balance": bank["balance"],

            "account": bank["account"],

            "card": bank["card"],

            "loan": bank["loan"],

            "loan_time": bank["loan_time"]

        }

    else:

        user["bank"] = {

            "balance": START_BANK,

            "account": None,

            "card": None,

            "loan": 0,

            "loan_time": 0

        }

    # ---------------- INVENTORY ----------------

    cursor.execute(
        """
        SELECT item, count
        FROM inventory
        WHERE user_id = ?
        """,
        (user["id"],)
    )

    inventory = []

    for item in cursor.fetchall():

        for _ in range(item["count"]):

            inventory.append(item["item"])

    user["inventory"] = inventory

    # ---------------- CRYPTO ----------------

    cursor.execute(
        """
        SELECT symbol, amount
        FROM crypto
        WHERE user_id = ?
        """,
        (user["id"],)
    )

    crypto = {}

    for coin in cursor.fetchall():

        crypto[coin["symbol"]] = coin["amount"]

    user["crypto"] = crypto

    return user


# ==================================================
# GAME ID
# ==================================================

def get_next_game_id():

    cursor.execute(
        "SELECT MAX(game_id) AS max_id FROM users"
    )

    row = cursor.fetchone()

    if row["max_id"] is None:

        return 1

    return row["max_id"] + 1


# ==================================================
# FIND USER
# ==================================================

def get_user_by_bale_id(bale_id):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE bale_id = ?
        """,
        (bale_id,)
    )

    return row_to_user(cursor.fetchone())


def get_user_by_game_id(game_id):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE game_id = ?
        """,
        (game_id,)
    )

    return row_to_user(cursor.fetchone())


def get_user_by_card(card):

    cursor.execute(
        """
        SELECT users.*
        FROM users
        JOIN bank
        ON users.id = bank.user_id
        WHERE bank.card = ?
        """,
        (card,)
    )

    return row_to_user(cursor.fetchone())


def get_user_by_account(account):

    cursor.execute(
        """
        SELECT users.*
        FROM users
        JOIN bank
        ON users.id = bank.user_id
        WHERE bank.account = ?
        """,
        (account,)
    )

    return row_to_user(cursor.fetchone())# ==================================================
# CREATE / UPDATE USER
# ==================================================

def create_user(bale_id, name):

    game_id = get_next_game_id()

    cursor.execute(
        """
        INSERT INTO users (

            game_id,
            bale_id,
            name,
            coin,
            gem,
            level,
            xp,
            job,
            last_work

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            game_id,
            bale_id,
            name,
            START_COIN,
            START_GEM,
            START_LEVEL,
            START_XP,
            None,
            0
        )
    )

    user_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO bank (

            user_id,
            balance,
            account,
            card,
            loan,
            loan_time

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            START_BANK,
            None,
            None,
            0,
            0
        )
    )

    cursor.execute(
        """
        INSERT INTO inventory (

            user_id,
            item,
            count

        )

        VALUES (?, ?, ?)
        """,
        (
            user_id,
            "داس",
            1
        )
    )

    conn.commit()

    return get_user_by_bale_id(bale_id)


def update_user(user):

    cursor.execute(
        """
        UPDATE users

        SET

            name = ?,
            coin = ?,
            gem = ?,
            level = ?,
            xp = ?,
            job = ?,
            last_work = ?

        WHERE bale_id = ?
        """,
        (
            user["name"],
            user["coin"],
            user["gem"],
            user["level"],
            user["xp"],
            user["job"],
            user["last_work"],
            user["bale_id"]
        )
    )

    cursor.execute(
        """
        UPDATE bank

        SET

            balance = ?,
            account = ?,
            card = ?,
            loan = ?,
            loan_time = ?

        WHERE user_id = ?
        """,
        (
            user["bank"]["balance"],
            user["bank"]["account"],
            user["bank"]["card"],
            user["bank"]["loan"],
            user["bank"]["loan_time"],
            user["id"]
        )
    )

    cursor.execute(
        "DELETE FROM inventory WHERE user_id = ?",
        (user["id"],)
    )

    items = {}

    for item in user["inventory"]:

        items[item] = items.get(item, 0) + 1

    for item, count in items.items():

        cursor.execute(
            """
            INSERT INTO inventory (

                user_id,
                item,
                count

            )

            VALUES (?, ?, ?)
            """,
            (
                user["id"],
                item,
                count
            )
        )

    cursor.execute(
        "DELETE FROM crypto WHERE user_id = ?",
        (user["id"],)
    )

    for symbol, amount in user["crypto"].items():

        cursor.execute(
            """
            INSERT INTO crypto (

                user_id,
                symbol,
                amount

            )

            VALUES (?, ?, ?)
            """,
            (
                user["id"],
                symbol,
                amount
            )
        )

    conn.commit()# ==================================================
# COIN SYSTEM
# ==================================================

def add_coin(user, amount):

    if amount <= 0:
        return False

    user["coin"] += amount

    update_user(user)

    return True


def remove_coin(user, amount):

    if amount <= 0:
        return False

    if user["coin"] < amount:
        return False

    user["coin"] -= amount

    update_user(user)

    return True


# ==================================================
# BANK SYSTEM
# ==================================================

def add_bank_money(user, amount):

    if amount <= 0:
        return False

    user["bank"]["balance"] += amount

    update_user(user)

    return True


def remove_bank_money(user, amount):

    if amount <= 0:
        return False

    if user["bank"]["balance"] < amount:
        return False

    user["bank"]["balance"] -= amount

    update_user(user)

    return True


def deposit_coin(user, amount):

    if amount <= 0:
        return False

    if user["coin"] < amount:
        return False

    user["coin"] -= amount

    user["bank"]["balance"] += amount

    update_user(user)

    return True


def withdraw_coin(user, amount):

    if amount <= 0:
        return False

    if user["bank"]["balance"] < amount:
        return False

    user["bank"]["balance"] -= amount

    user["coin"] += amount

    update_user(user)

    return True


def transfer_bank_money(sender, receiver, amount):

    if amount <= 0:
        return False

    if sender["bank"]["balance"] < amount:
        return False

    sender["bank"]["balance"] -= amount

    receiver["bank"]["balance"] += amount

    update_user(sender)

    update_user(receiver)

    return True


# ==================================================
# BANK ACCOUNT
# ==================================================

def set_bank_account(user, account):

    user["bank"]["account"] = account

    update_user(user)


def set_bank_card(user, card):

    user["bank"]["card"] = card

    update_user(user)


def set_loan(user, amount, loan_time):

    user["bank"]["loan"] = amount

    user["bank"]["loan_time"] = loan_time

    update_user(user)


def remove_loan(user):

    user["bank"]["loan"] = 0

    user["bank"]["loan_time"] = 0

    update_user(user)


# ==================================================
# CHECK SYSTEM
# ==================================================

def card_exists(card):

    return get_user_by_card(card) is not None


def account_exists(account):

    return get_user_by_account(account) is not None


def has_bank_account(user):

    return user["bank"]["account"] is not None


def has_bank_card(user):

    return user["bank"]["card"] is not None


def get_bank_balance(user):

    return user["bank"]["balance"]# ==================================================
# INVENTORY SYSTEM
# ==================================================

def has_item(user, item):

    return item in user["inventory"]


def add_item(user, item, count=1):

    if count <= 0:
        return False

    for _ in range(count):
        user["inventory"].append(item)

    update_user(user)

    return True


def remove_item(user, item, count=1):

    if count <= 0:
        return False

    if user["inventory"].count(item) < count:
        return False

    for _ in range(count):
        user["inventory"].remove(item)

    update_user(user)

    return True


def get_item_count(user, item):

    return user["inventory"].count(item)


def clear_inventory(user):

    user["inventory"].clear()

    update_user(user)


# ==================================================
# CRYPTO SYSTEM
# ==================================================

def get_crypto_amount(user, symbol):

    return user["crypto"].get(symbol.upper(), 0)


def set_crypto(user, symbol, amount):

    symbol = symbol.upper()

    if amount <= 0:

        user["crypto"].pop(symbol, None)

    else:

        user["crypto"][symbol] = amount

    update_user(user)


def add_crypto(user, symbol, amount):

    if amount <= 0:
        return False

    symbol = symbol.upper()

    user["crypto"][symbol] = (
        user["crypto"].get(symbol, 0) + amount
    )

    update_user(user)

    return True


def remove_crypto(user, symbol, amount):

    if amount <= 0:
        return False

    symbol = symbol.upper()

    current = user["crypto"].get(symbol, 0)

    if current < amount:
        return False

    current -= amount

    if current == 0:

        del user["crypto"][symbol]

    else:

        user["crypto"][symbol] = current

    update_user(user)

    return True


# ==================================================
# DATABASE TOOLS
# ==================================================

def commit():

    conn.commit()


def close():

    conn.commit()

    conn.close()# ==================================================
# TRANSACTION SYSTEM
# ==================================================

import time


def add_transaction(
    sender_id,
    receiver_id,
    amount,
    tx_type,
    tax=0
):

    cursor.execute(
        """
        INSERT INTO transactions (

            sender_id,
            receiver_id,
            amount,
            tax,
            type,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            sender_id,
            receiver_id,
            amount,
            tax,
            tx_type,
            int(time.time())
        )
    )

    conn.commit()


def get_transactions(user_id, limit=20):

    cursor.execute(
        """
        SELECT *

        FROM transactions

        WHERE
            sender_id = ?
            OR receiver_id = ?

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            user_id,
            user_id,
            limit
        )
    )

    return [dict(row) for row in cursor.fetchall()]


# ==================================================
# ADMIN LOG SYSTEM
# ==================================================

def add_admin_log(
    admin_id,
    action,
    target_id=None,
    amount=None
):

    cursor.execute(
        """
        INSERT INTO admin_logs (

            admin_id,
            action,
            target_id,
            amount,
            created_at

        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            admin_id,
            action,
            target_id,
            amount,
            int(time.time())
        )
    )

    conn.commit()


def get_admin_logs(limit=50):

    cursor.execute(
        """
        SELECT *

        FROM admin_logs

        ORDER BY id DESC

        LIMIT ?
        """,
        (limit,)
    )

    return [dict(row) for row in cursor.fetchall()]


# ==================================================
# USER LIST
# ==================================================

def get_all_users():

    cursor.execute(
        """
        SELECT *

        FROM users

        ORDER BY game_id
        """
    )

    return [
        row_to_user(row)
        for row in cursor.fetchall()
    ]


def get_user_count():

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM users
        """
    )

    return cursor.fetchone()[0]


# ==================================================
# DELETE USER
# ==================================================

def delete_user(bale_id):

    user = get_user_by_bale_id(bale_id)

    if user is None:
        return False

    cursor.execute(
        """
        DELETE FROM users

        WHERE bale_id = ?
        """,
        (bale_id,)
    )

    conn.commit()

    return True


# ==================================================
# DATABASE INFO
# ==================================================

def database_info():

    return {

        "database": DATABASE_NAME,

        "users": get_user_count()

    }

def __del__():

    try:
        conn.commit()
        conn.close()

    except:
        pass
