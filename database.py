import json
import os

from config import (
    START_COIN,
    START_GEM,
    START_LEVEL,
    START_XP,
    START_BANK
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "users.json")


# -------------------------
# LOAD / SAVE
# -------------------------

def load_users():

    if not os.path.exists(DATABASE_FILE):
        return []

    with open(
        DATABASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_users(users):

    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4,
            ensure_ascii=False
        )


# -------------------------
# GAME ID
# -------------------------

def get_next_game_id():

    users = load_users()

    if not users:
        return 1

    return max(
        user["game_id"]
        for user in users
    ) + 1


# -------------------------
# FIND USERS
# -------------------------

def get_user_by_bale_id(bale_id):

    users = load_users()

    for user in users:

        if user["bale_id"] == bale_id:
            return user

    return None


def get_user_by_game_id(game_id):

    users = load_users()

    for user in users:

        if user["game_id"] == game_id:
            return user

    return None


def get_user_by_card(card):

    users = load_users()

    for user in users:

        if user["bank"]["card"] == card:
            return user

    return None


def get_user_by_account(account):

    users = load_users()

    for user in users:

        if user["bank"]["account"] == account:
            return user

    return None


# -------------------------
# CREATE USER
# -------------------------

def create_user(bale_id, name):

    users = load_users()

    user = {

        "game_id": get_next_game_id(),

        "bale_id": bale_id,

        "name": name,

        # Economy

        "coin": START_COIN,
        "gem": START_GEM,

        # Level

        "level": START_LEVEL,
        "xp": START_XP,

        # Job

        "job": None,

        # Bank

        "bank": {

            "balance": START_BANK,

            "account": None,

            "card": None,

            "loan": 0,

            "loan_time": 0

        },

        # Items

        "inventory": [
            "داس"
        ],

        # Work

        "last_work": 0,

        # Crypto

        "crypto": {}

    }

    users.append(user)

    save_users(users)

    return user
    
    # -------------------------
# UPDATE USER
# -------------------------

def update_user(updated_user):

    users = load_users()

    for index, user in enumerate(users):

        if user["bale_id"] == updated_user["bale_id"]:

            users[index] = updated_user

            break

    save_users(users)


# -------------------------
# COIN SYSTEM
# -------------------------

def add_coin(user, amount):

    user["coin"] += amount

    update_user(user)


def remove_coin(user, amount):

    if amount <= 0:

        return False

    if user["coin"] < amount:

        return False

    user["coin"] -= amount

    update_user(user)

    return True


# -------------------------
# BANK SYSTEM
# -------------------------

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


def set_bank_account(user, account):

    user["bank"]["account"] = account

    update_user(user)


def set_bank_card(user, card):

    user["bank"]["card"] = card

    update_user(user)
    
    # -------------------------
# LOAN SYSTEM
# -------------------------

def set_loan(user, amount, loan_time):

    user["bank"]["loan"] = amount
    user["bank"]["loan_time"] = loan_time

    update_user(user)


def remove_loan(user):

    user["bank"]["loan"] = 0
    user["bank"]["loan_time"] = 0

    update_user(user)


# -------------------------
# CHECK SYSTEM
# -------------------------

def card_exists(card):

    return get_user_by_card(card) is not None


def account_exists(account):

    return get_user_by_account(account) is not None


# -------------------------
# ACCOUNT INFO
# -------------------------

def has_bank_account(user):

    return user["bank"]["account"] is not None


def has_bank_card(user):

    return user["bank"]["card"] is not None


def get_bank_balance(user):

    return user["bank"]["balance"]
    
    # -------------------------
# BANK TOOLS
# -------------------------

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
