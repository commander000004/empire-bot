# commands/shop.py

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
    }

}


async def shop(message):

    text = "🛒 فروشگاه Empire\n\n"

    for item, data in SHOP.items():

        text += (
            f"📦 {item}\n"
            f"💰 {data['price']} Coin\n\n"
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

    if user["coin"] < price:

        await message.reply(
            "❌ Coin کافی نداری."
        )

        return

    user["coin"] -= price
    user["inventory"].append(item)

    update_user(user)

    await message.reply(

        f"✅ خرید انجام شد.\n\n"

        f"📦 {item}\n"

        f"💰 {price} Coin"

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