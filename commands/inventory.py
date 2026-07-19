from bale import Message

from database import (
    get_user_by_bale_id,
    create_user
)


async def inventory_handler(bot, message: Message):

    user = get_user_by_bale_id(
        message.author.id
    )


    if user is None:

        user = create_user(
            message.author.id,
            message.author.first_name
        )


    inventory = user.get(
        "inventory",
        []
    )


    if not inventory:

        await bot.send_message(
            message.chat.id,
            "🎒 کیف شما خالی است."
        )

        return



    text = (
        "🎒 کیف آیتم‌های شما\n\n"
    )


    for item in inventory:

        text += (
            f"🔹 {item}\n"
        )


    text += (
        f"\n📦 تعداد آیتم‌ها: {len(inventory)}"
    )


    await bot.send_message(
        message.chat.id,
        text
    )