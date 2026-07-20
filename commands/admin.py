# commands/admin.py

from config import OWNERS

from database import (
    total_players,
    total_groups,
    total_banned,
    get_all_users,
    get_all_groups,
    set_user_value,
    get_user,
    set_ban
)


def is_owner(user_id):
    return int(user_id) in OWNERS


# ==========================
# Admin Panel
# ==========================

async def admin_panel(message):

    if not is_owner(message.author.id):
        return

    text = """
👑 پنل مدیریت Empire

━━━━━━━━━━━━━━

📊 آمار

آمار

━━━━━━━━━━━━━━

⚙️ تنظیم بازیکن

تنظیم کوین ID مقدار
تنظیم جم ID مقدار
تنظیم xp ID مقدار
تنظیم لول ID مقدار

━━━━━━━━━━━━━━

🚫 بن ID
✅ آنبن ID

━━━━━━━━━━━━━━

📢 همگانی متن پیام

━━━━━━━━━━━━━━

Empire V3
"""

    await message.reply(text)


# ==========================
# Stats
# ==========================

async def stats(message):

    if not is_owner(message.author.id):
        return

    users = get_all_users()

    total_coin = sum(u["coin"] for u in users)
    total_bank = sum(u["bank"] for u in users)
    total_gem = sum(u["gem"] for u in users)

    text = f"""
📊 آمار Empire

━━━━━━━━━━━━━━

👥 بازیکنان:
{total_players()}

👨‍👩‍👧‍👦 گروه‌ها:
{total_groups()}

🚫 بن شده:
{total_banned()}

━━━━━━━━━━━━━━

💰 Coin:
{total_coin:,}

🏦 Bank:
{total_bank:,}

💎 Gem:
{total_gem:,}
"""

    await message.reply(text)


# ==========================
# Set Player
# ==========================

async def set_player(
    message,
    mode,
    user_id,
    amount
):

    if not is_owner(message.author.id):
        return

    fields = {
        "کوین": "coin",
        "جم": "gem",
        "xp": "xp",
        "لول": "level"
    }

    if mode not in fields:

        await message.reply("❌ نوع تنظیم اشتباه است.")
        return

    user = get_user(str(user_id))

    if not user:

        await message.reply("❌ بازیکن پیدا نشد.")
        return

    ok = set_user_value(
        user_id,
        fields[mode],
        amount
    )

    if ok:

        await message.reply(
            f"✅ انجام شد.\n\n"
            f"{mode}: {amount}"
        )

    else:

        await message.reply("❌ خطا.")


# ==========================
# Ban
# ==========================

async def ban_user(message, user_id):

    if not is_owner(message.author.id):
        return

    if set_ban(user_id, True):

        await message.reply(
            f"🚫 {user_id} بن شد."
        )

    else:

        await message.reply(
            "❌ کاربر پیدا نشد."
        )


async def unban_user(message, user_id):

    if not is_owner(message.author.id):
        return

    if set_ban(user_id, False):

        await message.reply(
            f"✅ {user_id} آنبن شد."
        )

    else:

        await message.reply(
            "❌ کاربر پیدا نشد."
    )
        # ==========================
# Broadcast
# ==========================

async def broadcast(message, bot, text):

    if not is_owner(message.author.id):
        return

    groups = get_all_groups()

    success = 0
    failed = 0

    for group in groups:

        try:

            await bot.send_message(
                chat_id=group[0],
                text=text
            )

            success += 1

        except Exception as e:

            print(
                "Broadcast Error:",
                e
            )

            failed += 1

    await message.reply(

        f"📢 پیام همگانی ارسال شد.\n\n"
        f"✅ موفق: {success}\n"
        f"❌ ناموفق: {failed}"

    )

    print(
        f"[ADMIN] Broadcast by {message.author.id}"
                   )
