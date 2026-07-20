# commands/bank.py
import time

from database import (
    get_user,
    update_user,
    get_all_users,
    create_card
)


async def bank(message):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return

    now = int(time.time())

    if user["bank"] > 0 and now - user["last_interest"] >= 43200:

        interest = int(user["bank"] * 0.05)

        user["bank"] += interest

        user["last_interest"] = now

        update_user(user)

    card = user["card"] or "نداری"

    text = f"""
🏦 بانک Empire
📈 سود بانکی:
5٪ هر 12 ساعت

━━━━━━━━━━━━━━

💵 Coin:
{user["coin"]}

🏦 موجودی بانک:
{user["bank"]}

💳 کارت:
{card}

━━━━━━━━━━━━━━

دستورات:

ساخت کارت

واریز 1000

برداشت 1000

کارت به کارت EMP-123456 1000
"""

    await message.reply(text)


async def make_card(message):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        return

    if user["card"]:

        await message.reply(
            f"💳 کارت شما:\n{user['card']}"
        )

        return

    user["card"] = create_card()

    update_user(user)

    await message.reply(

        f"🎉 کارت بانکی ساخته شد.\n\n"

        f"💳 {user['card']}"

    )


async def deposit(message, amount):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        return

    if amount <= 0:

        await message.reply(
            "❌ مبلغ نامعتبر است."
        )

        return

    if user["coin"] < amount:

        await message.reply(
            "❌ Coin کافی نداری."
        )

        return

    user["coin"] -= amount

    user["bank"] += amount

    update_user(user)

    await message.reply(

        f"🏦 {amount} Coin "
        f"به بانک واریز شد."

    )


async def withdraw(message, amount):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        return

    if amount <= 0:

        await message.reply(
            "❌ مبلغ نامعتبر است."
        )

        return

    if user["bank"] < amount:

        await message.reply(
            "❌ موجودی بانک کافی نیست."
        )

        return

    user["bank"] -= amount

    user["coin"] += amount

    update_user(user)

    await message.reply(

        f"💰 {amount} Coin "
        f"برداشت شد."

    )


async def card_transfer(
    message,
    card,
    amount
):

    sender = get_user(
        str(message.author.id)
    )

    if not sender:

        return

    if not sender["card"]:

        await message.reply(
            "❌ اول کارت بساز."
        )

        return

    if sender["bank"] < amount:

        await message.reply(
            "❌ موجودی بانک کافی نیست."
        )

        return

    target = None

    for user in get_all_users():

        if user["card"] == card:

            target = user

            break

    if not target:

        await message.reply(
            "❌ کارت پیدا نشد."
        )

        return

    sender["bank"] -= amount

    target["bank"] += amount

    update_user(sender)
    update_user(target)

    await message.reply(

        f"✅ انتقال انجام شد.\n\n"

        f"💸 {amount} Coin"

    )
