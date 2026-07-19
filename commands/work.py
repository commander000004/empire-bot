import json
import random
import time

from bale import Message

from database import (
    get_user_by_bale_id,
    create_user,
    update_user
)

from utils.level import check_level_up


JOBS_FILE = "data/jobs.json"



def load_jobs():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)




def get_unlocked_jobs(level):

    jobs = load_jobs()

    unlocked = []

    for name, info in jobs.items():

        if info["level"] == level:

            unlocked.append(name)

    return unlocked





WORK_MESSAGES = {


    "کشاورز": [

        "🌾 امروز محصولاتت را برداشت کردی.",
        "🚜 چند ساعت در مزرعه کار کردی.",
        "🌽 فروش امروز معمولی بود.",
        "🥕 مشتری‌های خوبی پیدا کردی."

    ],


    "هیزم شکن": [

        "🪓 امروز در جنگل هیزم جمع کردی.",
        "🌲 چند درخت خشک را بریدی.",
        "🪵 سفارش هیزم تحویل دادی."

    ],


    "معدنچی": [

        "⛏ داخل معدن ساعت‌ها کار کردی.",
        "💎 سنگ‌های ارزشمند پیدا کردی.",
        "🪨 امروز معدن سخت بود."

    ],


    "ماهیگیر": [

        "🎣 امروز ماهی زیادی گرفتی.",
        "🌊 دریا آرام نبود ولی موفق شدی.",
        "🐟 صید خوبی داشتی."

    ]

}





async def work_handler(bot, message: Message):


    user = get_user_by_bale_id(
        message.author.id
    )


    if user is None:

        user = create_user(
            message.author.id,
            message.author.first_name
        )



    if user.get("job") is None:


        await bot.send_message(

            message.chat.id,

            "❌ هنوز شغلی انتخاب نکرده‌ای.\n\n"
            "اول دستور «شغل‌ها» را بزن."

        )

        return




    jobs = load_jobs()


    job_name = user["job"]


    job = jobs[job_name]





    # بررسی ابزار

    required_tool = job["tool"]


    inventory = user.get(
        "inventory",
        []
    )


    if required_tool not in inventory:


        await bot.send_message(

            message.chat.id,

            f"❌ ابزار لازم را نداری.\n\n"
            f"💼 شغل: {job_name}\n"
            f"🔧 نیاز به: {required_tool}\n\n"
            "🛒 از فروشگاه خرید کن."

        )

        return





    # بررسی کول داون

    now = int(time.time())


    last_work = user.get(
        "last_work",
        0
    )


    cooldown = job["cooldown"]



    if now - last_work < cooldown:


        remain = cooldown - (now - last_work)


        minutes = remain // 60

        seconds = remain % 60



        await bot.send_message(

            message.chat.id,

            f"⏳ هنوز آماده کار نیستی.\n\n"
            f"زمان باقی‌مانده: "
            f"{minutes} دقیقه و {seconds} ثانیه"

        )

        return





    # درآمد

    coin = random.randint(

        job["coin_min"],

        job["coin_max"]

    )


    xp = job["xp"]




    user["coin"] += coin

    user["xp"] += xp

    user["last_work"] = now





    # لول آپ

    level_up = check_level_up(
        user
    )


    new_jobs = []


    if level_up:

        new_jobs = get_unlocked_jobs(
            user["level"]
        )





    update_user(user)





    text = random.choice(

        WORK_MESSAGES.get(

            job_name,

            [
                "💼 امروز کار خوبی انجام دادی."
            ]

        )

    )



    level_text = ""



    if level_up:


        level_text += (

            "\n\n🎉 تبریک!\n"

            f"⭐ سطح شما به {user['level']} رسید!"

        )



    if new_jobs:


        level_text += (

            "\n\n🔓 شغل‌های جدید باز شد:\n"

        )


        for new_job in new_jobs:

            level_text += (

                f"💼 {new_job}\n"

            )





    await bot.send_message(

        message.chat.id,


        f"""
{text}


💼 شغل:
{job_name}


💰 درآمد:
+{coin} کوین


✨ XP:
+{xp}

{level_text}
"""

    )