import random
import time

from database import (
    get_user,
    update_user
)

MISSIONS = [

    {
        "id": "work3",
        "name": "۳ بار کار کن",
        "type": "work",
        "target": 3,
        "coin": 1000,
        "gem": 1,
        "xp": 20
    },

    {
        "id": "work5",
        "name": "۵ بار کار کن",
        "type": "work",
        "target": 5,
        "coin": 2500,
        "gem": 2,
        "xp": 40
    },

    {
        "id": "xp50",
        "name": "۵۰ XP کسب کن",
        "type": "xp",
        "target": 50,
        "coin": 1500,
        "gem": 1,
        "xp": 25
    },

    {
        "id": "xp100",
        "name": "۱۰۰ XP کسب کن",
        "type": "xp",
        "target": 100,
        "coin": 3000,
        "gem": 2,
        "xp": 50
    },

    {
        "id": "coin5000",
        "name": "۵۰۰۰ Coin کسب کن",
        "type": "coin",
        "target": 5000,
        "coin": 2000,
        "gem": 1,
        "xp": 30
    },

    {
        "id": "coin10000",
        "name": "۱۰۰۰۰ Coin کسب کن",
        "type": "coin",
        "target": 10000,
        "coin": 4000,
        "gem": 2,
        "xp": 60
    },

    {
        "id": "buy1",
        "name": "۱ آیتم بخر",
        "type": "buy",
        "target": 1,
        "coin": 1500,
        "gem": 1,
        "xp": 20
    },

    {
        "id": "food1",
        "name": "۱ غذا مصرف کن",
        "type": "food",
        "target": 1,
        "coin": 1000,
        "gem": 1,
        "xp": 15
    },

    {
        "id": "food2",
        "name": "۲ غذا مصرف کن",
        "type": "food",
        "target": 2,
        "coin": 2500,
        "gem": 2,
        "xp": 30
    }

]


def generate_daily_missions(user):

    selected = random.sample(MISSIONS, 3)

    user["daily_missions"] = []

    for mission in selected:

        user["daily_missions"].append({

            "id": mission["id"],
            "name": mission["name"],
            "type": mission["type"],
            "target": mission["target"],
            "progress": 0,
            "done": False,
            "coin": mission["coin"],
            "gem": mission["gem"],
            "xp": mission["xp"]

        })

    user["daily_bonus"] = False
    user["daily_reset"] = int(time.time() // 86400)


def check_daily_reset(user):

    today = int(time.time() // 86400)

    if user.get("daily_reset", -1) != today:

        generate_daily_missions(user)

        update_user(user)

        return True

    return False


async def mission(message):

    user = get_user(str(message.author.id))

    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return

    check_daily_reset(user)

    text = "🎯 چالش‌های روزانه\n\n"

    completed = 0

    for m in user["daily_missions"]:

        if m["done"]:
            completed += 1
            status = "✅"
        else:
            status = "⏳"

        text += (
            f"{status} {m['name']}\n"
            f"📈 {m['progress']}/{m['target']}\n"
            f"🎁 {m['coin']} Coin | {m['gem']} Gem | {m['xp']} XP\n\n"
        )

    if completed == 3:

        if not user["daily_bonus"]:

            user["coin"] += 5000
            user["gem"] += 3
            user["xp"] += 100

            user["daily_bonus"] = True

            update_user(user)

            text += (
                "🎉 هر ۳ مأموریت انجام شد!\n\n"
                "🏆 جایزه ویژه دریافت کردی:\n"
                "💰 5000 Coin\n"
                "💎 3 Gem\n"
                "✨ 100 XP\n\n"
            )

        else:

            text += (
                "🏆 جایزه ویژه امروز را قبلاً دریافت کرده‌ای.\n\n"
            )

    remain = 86400 - (int(time.time()) % 86400)

    h = remain // 3600
    m = (remain % 3600) // 60

    text += f"⏳ ریست بعدی: {h}h {m}m"

    await message.reply(text)

def update_mission(user, mission_type, amount=1):

    if "daily_missions" not in user:
        return


    for mission in user["daily_missions"]:

        if mission["done"]:
            continue


        if mission["type"] != mission_type:
            continue


        mission["progress"] += amount


        if mission["progress"] >= mission["target"]:

            mission["progress"] = mission["target"]

            mission["done"] = True


            user["coin"] += mission["coin"]

            user["gem"] += mission["gem"]

            user["xp"] += mission["xp"]


    # بررسی جایزه کامل کردن همه مأموریت‌ها

    all_done = True

    for mission in user["daily_missions"]:

        if not mission["done"]:
            all_done = False
            break


    if all_done and not user.get("daily_bonus", False):

        user["coin"] += 5000

        user["gem"] += 3

        user["xp"] += 100

        user["daily_bonus"] = True
