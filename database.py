import json
import os

from config import (
    START_COIN,
    START_GEM,
    START_LEVEL,
    START_XP,
    START_BANK
)


DATABASE_FILE = "users.json"



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



def get_next_game_id():

    users = load_users()

    if not users:
        return 1

    return max(
        user["game_id"]
        for user in users
    ) + 1



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


        # Finance

        "bank": START_BANK,


        # Items

        "inventory": [
            "داس"
        ],


        # Work system

        "last_work": 0,


        # Crypto

        "crypto": {}

    }


    users.append(user)

    save_users(users)


    return user



def update_user(updated_user):

    users = load_users()


    for index, user in enumerate(users):

        if user["bale_id"] == updated_user["bale_id"]:

            users[index] = updated_user

            break


    save_users(users)
