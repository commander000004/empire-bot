# commands/shop.py
import time

from database import (
    get_user,
    update_user
)


SHOP = {

    "غذا": {
        "price": 300
    },

    "داس": {
        "price": 1
    },

    "کلنگ": {
        "price": 2500
    },

    "چوب ماهیگیری": {
        "price": 3500
    },

    "چکش": {
        "price": 5000
    },

    "لپتاپ": {
        "price": 15000
    },

    "⏳ Time Booster": {
    "price": 50,
    "currency": "gem"
},

    "💰 Double Rewards": {
    "price": 100,
    "currency": "gem"
}

}


async def shop(message):

    text = "🛒 فروشگاه Empire\n\n"

    for item, data in SHOP.items():

        text += (
            f"📦 {item}\n"
            f"{'💎' if data.get('currency') == 'gem' else '💰'} {data['price']} {'Gem' if data.get('currency') == 'gem' else 'Coin'}\n\n"
        )

    text += (
        "━━━━━━━━━━━━━━\n"
        "برای خرید:\n"
        "خرید غذا"
    )

    await message.reply(text)


async def buy(message, item):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return

    if item not in SHOP:

        await message.reply(
            "❌ این آیتم وجود ندارد."
        )

        return

    price = SHOP[item]["price"]

    currency = SHOP[item].get(
        "currency",
        "coin"
    )

    if currency == "gem":

        if user["gem"] < price:

            await message.reply(
                "❌ Gem کافی نداری."
            )

            return

        user["gem"] -= price

    else:

        if user["coin"] < price:

            await message.reply(
                "❌ Coin کافی نداری."
            )

            return

        user["coin"] -= price

    # فعال کردن بوسترها
    if item == "⏳ Time Booster":

        user["time_booster_until"] = int(time.time()) + (12 * 60 * 60)

    elif item == "💰 Double Rewards":

        user["double_rewards_until"] = int(time.time()) + (12 * 60 * 60)

    else:

        user["inventory"].append(item)

    update_user(user)

    await message.reply(

        f"✅ خرید انجام شد.\n\n"
        f"📦 {item}\n"
        f"{'💎' if currency == 'gem' else '💰'} {price} {'Gem' if currency == 'gem' else 'Coin'}"

        )


async def inventory(message):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        return

    if not user["inventory"]:

        await message.reply(
            "🎒 کیف شما خالی است."
        )

        return

    text = "🎒 کیف شما\n\n"

    items = {}

    for item in user["inventory"]:

        items[item] = items.get(item, 0) + 1

    for item, count in items.items():

        text += f"📦 {item} × {count}\n"

    await message.reply(text)
