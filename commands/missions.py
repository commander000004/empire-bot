from database import get_user, update_user


MISSIONS = {

    "کار": {
        "need": 5,
        "reward_coin": 3000,
        "reward_xp": 100
    },

    "خرید": {
        "need": 1,
        "reward_coin": 500,
        "reward_xp": 20
    }

}



async def missions(message):

    user_id = str(message.author.id)

    user = get_user(user_id)


    if not user:

        await message.reply(
            "❌ اول پروفایل بساز."
        )

        return



    text = (
        "🎯 ماموریت‌های Empire\n\n"
        "1️⃣ انجام کار\n"
        "پیشرفت: 0/5\n\n"
        "2️⃣ خرید آیتم\n"
        "پیشرفت: 0/1\n\n"
        "🔥 به زودی ماموریت‌های بیشتر!"
    )


    await message.reply(text)