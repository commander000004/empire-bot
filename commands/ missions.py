# commands/missions.py

import time

from database import (
    get_user,
    update_user
)


MISSIONS = [

    {
        "name": "یک بار کار کن",
        "need": 1,
        "reward_coin": 500,
        "reward_xp": 20
    },

    {
        "name": "سه بار کار کن",
        "need": 3,
        "reward_coin": 1500,
        "reward_xp": 50
    },

    {
        "name": "پنج بار کار کن",
        "need": 5,
        "reward_coin": 3000,
        "reward_xp": 100
    }

]


async def missions(message):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return

    count = user["work_count"]

    text = "🎯 ماموریت‌های امروز\n\n"

    for mission in MISSIONS:

        done = "✅" if count >= mission["need"] else "❌"

        text += (
            f"{done} {mission['name']}\n"
            f"📈 پیشرفت: {min(count, mission['need'])}/{mission['need']}\n"
            f"💰 {mission['reward_coin']} Coin\n"
            f"✨ {mission['reward_xp']} XP\n\n"
        )

    text += (
        "━━━━━━━━━━━━━━\n"
        "🎁 برای دریافت جایزه:\n"
        "دریافت جایزه"
    )

    await message.reply(text)


async def claim_reward(message):

    user = get_user(
        str(message.author.id)
    )

    if not user:

        return

    count = user["work_count"]

    reward = None

    for mission in reversed(MISSIONS):

        if count >= mission["need"]:

            reward = mission

            break

    if not reward:

        await message.reply(
            "❌ هنوز هیچ ماموریتی را کامل نکرده‌ای."
        )

        return

    user["coin"] += reward["reward_coin"]
    user["xp"] += reward["reward_xp"]

    # ریست ماموریت
    user["work_count"] = 0

    update_user(user)

    await message.reply(

        f"🎉 جایزه ماموریت دریافت شد.\n\n"

        f"💰 +{reward['reward_coin']} Coin\n"

        f"✨ +{reward['reward_xp']} XP"

    )