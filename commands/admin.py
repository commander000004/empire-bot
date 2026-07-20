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


# ==========================
# Check Owner
# ==========================

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

⚙️ تنظیم بازیکن:

تنظیم کوین ID مقدار

تنظیم جم ID مقدار

تنظیم xp ID مقدار

تنظیم لول ID مقدار


مثال:

تنظیم کوین 123456 50000


━━━━━━━━━━━━━━

🚧 امکانات آینده:

📢 پیام همگانی

🚫 بن بازیکن

✅ آنبن

📝 لاگ‌ها


━━━━━━━━━━━━━━

Empire V3
v3 powered by @commander04
"""


    await message.reply(text)



# ==========================
# Stats
# ==========================

async def stats(message):

    if not is_owner(message.author.id):

        return


    users = get_all_users()


    total_coin = 0
    total_bank = 0
    total_gem = 0


    for user in users:

        total_coin += user["coin"]
        total_bank += user["bank"]
        total_gem += user["gem"]



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

💰 Coin کل:
{total_coin:,}

🏦 بانک کل:
{total_bank:,}

💎 Gem کل:
{total_gem:,}


━━━━━━━━━━━━━━

👑 Owner Panel
"""


    print(
        f"[ADMIN] {message.author.id} opened stats"
    )


    await message.reply(text)



# ==========================
# Set Player Value
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


        await message.reply(
            "❌ نوع تنظیم اشتباه است."
        )

        return



    user = get_user(
        str(user_id)
    )


    if not user:


        await message.reply(
            "❌ بازیکن پیدا نشد."
        )

        return



    result = set_user_value(

        user_id,

        fields[mode],

        amount

    )



    if result:


        await message.reply(

            f"✅ تغییر انجام شد\n\n"

            f"👤 بازیکن: {user_id}\n"

            f"⚙️ بخش: {mode}\n"

            f"🔢 مقدار جدید: {amount}"

        )


        print(

            f"[ADMIN LOG] "
            f"{message.author.id} "
            f"SET {mode} "
            f"{user_id} = {amount}"

        )



    else:


        await message.reply(
            "❌ خطا در تغییر اطلاعات."
        )
        # ==========================
# Ban / Unban
# ==========================


async def ban_user(message, user_id):

    if not is_owner(message.author.id):

        return


    result = set_ban(
        user_id,
        1
    )


    if result:

        await message.reply(
            f"🚫 کاربر {user_id} بن شد."
        )

    else:

        await message.reply(
            "❌ کاربر پیدا نشد."
        )




async def unban_user(message, user_id):

    if not is_owner(message.author.id):

        return


    result = set_ban(
        user_id,
        0
    )


    if result:

        await message.reply(
            f"✅ کاربر {user_id} آنبن شد."
        )

    else:

        await message.reply(
            "❌ کاربر پیدا نشد."
        )
        
        # ==========================
# Broadcast To Groups
# ==========================

async def broadcast(message, bot, text):

    if not is_owner(message.author.id):

        return
        
        print("Broadcast function reached")


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

        f"📢 پیام همگانی ارسال شد\n\n"
        f"✅ موفق: {success} گروه\n"
        f"❌ ناموفق: {failed} گروه"

    )


    print(
        f"[ADMIN LOG] Broadcast by {message.author.id}"
    )