# commands/work.py

import random
import time

from database import (
    get_user,
    update_user
)

from commands.jobs import JOBS

from level import (
    xp_need,
    check_level
)

GEM_CHANCE = 0.015

TEXTS = {

    "کشاورز": [
        "🌾 زمین را شخم زدید.",
        "🌱 بذر کاشتید.",
        "🚜 محصول را برداشت کردید.",
        "🛒 محصول را به فروشنده فروختید."
    ],

    "معدنچی": [
        "⛏ وارد معدن شدید.",
        "💎 سنگ‌های ارزشمند استخراج کردید.",
        "🚚 مواد معدنی را حمل کردید.",
        "💰 سنگ‌ها را فروختید."
    ],

    "فروشنده": [
        "🏪 مغازه را باز کردید.",
        "🤝 با مشتری‌ها معامله کردید.",
        "📦 سفارش‌ها را تحویل دادید.",
        "💵 سود خوبی کسب کردید."
    ],

    "ماهیگیر": [
        "🎣 تور را داخل آب انداختید.",
        "🐟 ماهی‌های تازه صید کردید.",
        "🚤 به ساحل برگشتید.",
        "💰 ماهی‌ها را فروختید."
    ],

    "آهنگر": [
        "🔥 کوره را روشن کردید.",
        "🔨 آهن را شکل دادید.",
        "⚔ تجهیزات ساختید.",
        "💰 محصولات را فروختید."
    ],

    "برنامه‌نویس": [
        "💻 پروژه جدید گرفتید.",
        "⌨ کدنویسی کردید.",
        "🐞 باگ‌ها را رفع کردید.",
        "💸 دستمزد دریافت کردید."
    ],

    "مدیر شرکت": [
        "🏢 جلسه برگزار کردید.",
        "📈 سود شرکت را افزایش دادید.",
        "🤝 قرارداد امضا کردید.",
        "💰 درآمد شرکت را دریافت کردید."
    ]

}


async def work(message):

    user = get_user(str(message.author.id))

    if not user:
        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )
        return

    if not user["job"]:
        await message.reply(
            "❌ ابتدا یک شغل انتخاب کن."
        )
        return

    job_name = user["job"]
    job = JOBS[job_name]

    now = int(time.time())

    cooldown = job["cooldown"]

    if user["time_booster_until"] > now:
        cooldown = cooldown // 2

    remain = cooldown - (
        now - user["last_work"]
    )

    if remain > 0:

        await message.reply(

            f"⏳ هنوز خسته‌ای!\n\n"
            f"🕒 {remain//60} دقیقه و "
            f"{remain%60} ثانیه دیگر."

        )

        return

    user["last_work"] = now

    user["work_count"] += 1

    food_used = 0

    if user["work_count"] >= job["food"]:

        if "غذا" in user["inventory"]:

            user["inventory"].remove("غذا")

            user["work_count"] = 0

            food_used = 1

        elif user["gem"] > 0:

            user["gem"] -= 1

            user["work_count"] = 0

        else:

            user["xp"] = max(
                0,
                user["xp"] - 10
            )

            await message.reply(
                "🍞 غذای شما تمام شده!\n"
                "❌ غذا بخرید یا از جم استفاده کنید.\n"
                "✨ 10 XP از شما کم شد."
            )

            return

    coin = random.randint(
        job["reward_min"],
        job["reward_max"]
    )

    xp = random.randint(
        job["xp_min"],
        job["xp_max"]
    )

    if user["double_rewards_until"] > now:
        coin *= 2
        xp *= 2

    user["coin"] += coin
    user["xp"] += xp

    got_gem = False

    if random.random() <= GEM_CHANCE:

        user["gem"] += 1

        got_gem = True

    level_up = check_level(user)

    update_user(user)

    text = ""

    for line in TEXTS[job_name]:

        text += line + "\n"

    text += "\n"

    text += f"🍞 غذا مصرف شده: {food_used}\n\n"

    text += f"💰 درآمد: +{coin} Coin\n"

    text += f"✨ تجربه: +{xp} XP\n\n"
      
    if got_gem:

        text += "💎 خوش‌شانس بودی! +1 Gem پیدا کردی.\n\n"

    if user["time_booster_until"] > now:

        remain_time = user["time_booster_until"] - now

        hours = remain_time // 3600

        minutes = (remain_time % 3600) // 60

        text += (
            f"⏳ Time Booster فعال: "
            f"{hours}h {minutes}m\n"
        )

    if user["double_rewards_until"] > now:

        remain_time = user["double_rewards_until"] - now

        hours = remain_time // 3600

        minutes = (remain_time % 3600) // 60

        text += (
            f"💰 Double Rewards فعال: "
            f"{hours}h {minutes}m\n"
        )

    text += "\n"

    text += (
        f"📈 XP: "
        f"{user['xp']}/"
        f"{xp_need(user['level'])}\n"
    )

    text += (
        f"⭐ Level: "
        f"{user['level']}"
    )

    if level_up:

        text += (

            "\n\n🎉 LEVEL UP!\n"
            f"⭐ Level جدید: {user['level']}"

        )

    await message.reply(text)
