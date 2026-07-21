import os
import json
import random
from contextlib import contextmanager

import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable not found."
    )


@contextmanager
def connect():

    conn = psycopg.connect(
        DATABASE_URL
    )

    try:

        yield conn

    finally:

        conn.close()


def init_db():

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users(

                    bale_id TEXT PRIMARY KEY,

                    name TEXT NOT NULL,

                    coin INTEGER NOT NULL,

                    gem INTEGER NOT NULL,

                    level INTEGER NOT NULL,

                    xp INTEGER NOT NULL,

                    last_work BIGINT NOT NULL,
                    
                    last_interest BIGINT NOT NULL,

                    bank INTEGER NOT NULL,

                    card TEXT,

                    inventory TEXT NOT NULL,

                    job TEXT,

                    work_count INTEGER NOT NULL,

                    banned BOOLEAN NOT NULL DEFAULT FALSE

                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS groups(

                    chat_id TEXT PRIMARY KEY,

                    title TEXT NOT NULL

                )
                """
            )

        db.commit()


def row_to_user(row):

    if row is None:

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

        "inventory": json.loads(
            row[9]
        ),

        "job": row[10],

        "work_count": row[11],

        "banned": bool(
            row[12]
        ),
        
        "last_interest": row[13],

        "time_booster_until": row[14],

        "double_rewards_until": row[15]

    }


def get_user(
    bale_id
):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """
                SELECT *
                FROM users
                WHERE bale_id=%s
                """,

                (
                    str(bale_id),
                )

            )

            row = cur.fetchone()

    return row_to_user(
        row
    )


def get_all_users():

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """
                SELECT *
                FROM users
                ORDER BY level DESC,
                         xp DESC
                """

            )

            rows = cur.fetchall()

    return [

        row_to_user(row)

        for row in rows

    ]


def create_user(
    bale_id,
    name
):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """
                INSERT INTO users(

                    bale_id,
                    name,
                    coin,
                    gem,
                    level,
                    xp,
                    last_work,
                    bank,
                    card,
                    inventory,
                    job,
                    work_count,
                    banned,
                    last_interest,
                    time_booster_until,
                    double_rewards_until

                )

                VALUES(

                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s 

                )
                """,

                (

                    str(bale_id),

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

                    False,
                    
                    0,

                    0,

                    0


                )

            )

            db.commit()


def update_user(user):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """
                UPDATE users

                SET

                    name=%s,

                    coin=%s,

                    gem=%s,

                    level=%s,

                    xp=%s,

                    last_work=%s,

                    bank=%s,

                    card=%s,

                    inventory=%s,

                    job=%s,

                    work_count=%s,

                    banned=%s,
                    
                    last_interest=%s,

                    time_booster_until=%s,

                    double_rewards_until=%s

                WHERE bale_id=%s
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

                    bool(user["banned"]),
                    
                    user["last_interest"],

                    user["time_booster_until"],

                    user["double_rewards_until"],

                    user["bale_id"]

                )

            )

        db.commit()


def add_group(chat_id, title):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """
                INSERT INTO groups(chat_id, title)

                VALUES(%s, %s)

                ON CONFLICT(chat_id)

                DO NOTHING
                """,

                (

                    str(chat_id),

                    title

                )

            )

        db.commit()


def get_all_groups():

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                "SELECT chat_id, title FROM groups"

            )

            return cur.fetchall()


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

            user

            for user in get_all_users()

            if user["banned"]

        ]

    )


def create_card():

    return "EMP-" + str(

        random.randint(

            100000,

            999999

        )

    )


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

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                f"""

                UPDATE users

                SET {field}=%s

                WHERE bale_id=%s

                """,

                (

                    value,

                    str(bale_id)

                )

            )

            changed = cur.rowcount

        db.commit()

    return changed > 0


def set_ban(

    bale_id,

    status

):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """

                UPDATE users

                SET banned=%s

                WHERE bale_id=%s

                """,

                (

                    bool(status),

                    str(bale_id)

                )

            )

            changed = cur.rowcount

        db.commit()

    return changed > 0


def user_exists(

    bale_id

):

    return get_user(
        bale_id
    ) is not None


def delete_user(

    bale_id

):

    with connect() as db:

        with db.cursor() as cur:

            cur.execute(

                """

                DELETE FROM users

                WHERE bale_id=%s

                """,

                (

                    str(bale_id),

                )

            )

        db.commit()


def get_user_by_bale_id(

    bale_id

):

    return get_user(
        bale_id
    )


def create_or_get_user(

    bale_id,

    name

):

    user = get_user(
        bale_id
    )

    if user:

        return user

    create_user(
        bale_id,
        name
    )

    return get_user(
        bale_id
            )
