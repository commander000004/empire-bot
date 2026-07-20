# commands/leaderboard.py

from database import get_all_users


def sort_users(users, key):

    return sorted(
        users,
        key=lambda x: x[key],
        reverse=True
    )


async def leaderboard(message):

    users = get_all_users()

    users = sorted(
        users,
        key=lambda x: x["coin"] + x["bank"],
        reverse=True
    )

    await send_board(
        message,
        users,
        "🏆 لیدربورد ثروت",
        "💰",
        lambda u: f"{u['coin'] + u['bank']:,} Coin"
    )


async def leaderboard_level(message):

    users = sort_users(
        get_all_users(),
        "level"
    )

    await send_board(
        message,
        users,
        "⭐ لیدربورد لول",
        "⭐",
        lambda u: f"Level {u['level']}"
    )


async def leaderboard_xp(message):

    users = sort_users(
        get_all_users(),
        "xp"
    )

    await send_board(
        message,
        users,
        "✨ لیدربورد XP",
        "✨",
        lambda u: f"{u['xp']} XP"
    )


async def leaderboard_gem(message):

    users = sort_users(
        get_all_users(),
        "gem"
    )

    await send_board(
        message,
        users,
        "💎 لیدربورد جم",
        "💎",
        lambda u: f"{u['gem']} Gem"
    )


async def send_board(
    message,
    users,
    title,
    emoji,
    value
):

    text = f"{title}\n\n"

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for i, user in enumerate(users[:10]):

        if i < 3:
            rank = medals[i]
        else:
            rank = f"{i+1}."

        text += (
            f"{rank} {user['name']}\n"
            f"{emoji} {value(user)}\n\n"
        )

    if len(users) == 0:

        text += "❌ هنوز بازیکنی وجود ندارد."

    await message.reply(text)