from database import get_user
import json



async def inventory(message):

    user_id = str(message.author.id)

    user = get_user(user_id)


    if not user:

        await message.reply(
            "اول پروفایل بساز."
        )

        return



    items = json.loads(
        user[8]
    )


    if not items:

        await message.reply(
            "🎒 کیف شما خالی است."
        )

        return



    text = "🎒 کیف شما:\n\n"


    for item in items:

        text += f"🔹 {item}\n"



    text += (
        f"\n📦 تعداد آیتم: {len(items)}"
    )


    await message.reply(text)