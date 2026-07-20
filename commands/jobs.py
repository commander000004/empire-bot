# commands/jobs.py

from database import (
    get_user,
    create_user,
    update_user
)


JOBS = {

    "کشاورز": {
        "level": 1,
        "item": "داس",
        "reward_min": 100,
        "reward_max": 150,
        "xp_min": 5,
        "xp_max": 13,
        "cooldown": 180,
        "food": 2
    },


    "معدنچی": {
        "level": 2,
        "item": "کلنگ",
        "reward_min": 150,
        "reward_max": 300,
        "xp_min": 13,
        "xp_max": 30,
        "cooldown": 300,
        "food": 2
    },


    "فروشنده": {
        "level": 3,
        "item": None,
        "reward_min": 300,
        "reward_max": 550,
        "xp_min": 35,
        "xp_max": 50,
        "cooldown": 420,
        "food": 3
    },


    "ماهیگیر": {
        "level": 5,
        "item": "چوب ماهیگیری",
        "reward_min": 600,
        "reward_max": 800,
        "xp_min": 40,
        "xp_max": 60,
        "cooldown": 600,
        "food": 3
    },


    "آهنگر": {
        "level": 7,
        "item": "چکش",
        "reward_min": 1000,
        "reward_max": 1500,
        "xp_min": 70,
        "xp_max": 100,
        "cooldown": 800,
        "food": 4
    },


    "برنامه‌نویس": {
        "level": 10,
        "item": "لپتاپ",
        "reward_min": 1000,
        "reward_max": 3000,
        "xp_min": 90,
        "xp_max": 130,
        "cooldown": 1000,
        "food": 4
    },


    "مدیر شرکت": {
        "level": 15,
        "item": "لپتاپ",
        "reward_min": 4000,
        "reward_max": 6000,
        "xp_min": 150,
        "xp_max": 220,
        "cooldown": 1100,
        "food": 5
    }

}



async def jobs(message):

    text = "👷 شغل‌های Empire\n\n"

    for name, data in JOBS.items():

        need = ""

        if data["item"]:
            need = f"🛠 نیاز: {data['item']}\n"


        text += (
            f"👔 {name}\n"
            f"🔓 Level: {data['level']}\n"
            f"{need}"
            f"💰 درآمد: {data['reward_min']} تا {data['reward_max']} Coin\n"
            f"✨ XP: {data['xp_min']} تا {data['xp_max']}\n\n"
        )


    text += "📌 انتخاب:\nانتخاب کشاورز"


    await message.reply(text)




async def choose_job(message, job):

    user_id = str(message.author.id)

    user = get_user(user_id)


    if not user:

        create_user(
            user_id,
            message.author.first_name
        )

        user = get_user(user_id)



    if job not in JOBS:

        await message.reply(
            "❌ چنین شغلی وجود ندارد."
        )

        return



    data = JOBS[job]


    if user["level"] < data["level"]:

        await message.reply(
            f"🔒 برای این شغل باید Level {data['level']} باشی."
        )

        return



    if data["item"]:

        if data["item"] not in user["inventory"]:

            await message.reply(
                f"❌ برای شغل {job} این آیتم لازم است:\n\n"
                f"🛒 وارد فروشگاه شو\n"
                f"📦 آیتم «{data['item']}» را خریداری کن."
            )

            return



    user["job"] = job

    update_user(user)


    await message.reply(
        f"🎉 شغل جدید انتخاب شد!\n\n"
        f"👷 {job}"
    )
