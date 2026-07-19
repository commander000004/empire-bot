import json

from bale import Message

from database import (
    get_user_by_bale_id,
    create_user,
    update_user
)


ITEMS_FILE = "data/items.json"



def load_items():

    with open(
        ITEMS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)




async def shop_handler(bot, message: Message):

    items = load_items()


    text = "🛒 فروشگاه Empire\n\n"


    for name, info in items.items():


        if info["coin"] == 0 and info["gem"] == 0:

            price = "🎁 رایگان"


        elif info["gem"] > 0:

            price = (
                f"💰 {info['coin']} Coin\n"
                f"💎 یا {info['gem']} Gem"
            )


        else:

            price = f"💰 {info['coin']} Coin"



        text += (

            f"🔹 {name}\n"
            f"{price}\n"
            f"📌 {info['description']}\n\n"

        )


    text += (
        "━━━━━━━━━━━━━━\n"
        "برای خرید:\n"
        "خرید [نام آیتم]\n\n"
        "مثال:\n"
        "خرید تبر"
    )


    await bot.send_message(
        message.chat.id,
        text
    )





async def buy_item(bot, message, item_name):


    items = load_items()


    if item_name not in items:


        await bot.send_message(

            message.chat.id,

            "❌ این آیتم وجود ندارد."

        )

        return



    user = get_user_by_bale_id(
        message.author.id
    )


    if user is None:


        user = create_user(

            message.author.id,

            message.author.first_name

        )



    item = items[item_name]


    inventory = user.get(
        "inventory",
        []
    )



    if item_name in inventory:


        await bot.send_message(

            message.chat.id,

            "❌ این آیتم را قبلاً داری."

        )

        return



    coin_price = item["coin"]

    gem_price = item["gem"]



    # خرید با کوین

    if user["coin"] >= coin_price:


        user["coin"] -= coin_price



    # خرید با جم

    elif gem_price > 0 and user["gem"] >= gem_price:


        user["gem"] -= gem_price



    else:


        await bot.send_message(

            message.chat.id,

            "❌ موجودی کافی نداری."

        )

        return




    inventory.append(
        item_name
    )


    user["inventory"] = inventory


    update_user(user)



    await bot.send_message(

        message.chat.id,

        f"✅ خرید موفق!\n\n"
        f"🎁 آیتم دریافت شد:\n"
        f"{item_name}"

    )





async def buy_command(bot, message):


    text = message.content.strip()


    item_name = text.replace(
        "خرید ",
        ""
    )


    await buy_item(

        bot,

        message,

        item_name

    )