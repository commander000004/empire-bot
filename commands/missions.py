# commands/missions.py

import random
import time

from database import (
    get_user,
    update_user
)


MISSIONS = [

    {
        "name": "۵ بار کار کن",
        "type": "work",
        "goal": 5,
        "reward_coin": 1500,
        "reward_xp": 30
    },

    {
        "name": "۱۰ بار کار کن",
        "type": "work",
        "goal": 10,
        "reward_coin": 3500,
        "reward_xp": 60
    },

    {
        "name": "۱۵ بار کار کن",
        "type": "work",
        "goal": 15,
        "reward_coin": 6000,
        "reward_xp": 100
    },

    {
        "name": "۵۰ XP کسب کن",
        "type": "xp",
        "goal": 50,
        "reward_coin": 2000,
        "reward_xp": 40
    },

    {
        "name": "۵۰۰۰ Coin کسب کن",
        "type": "coin",
        "goal": 5000,
        "reward_coin": 2500,
        "reward_xp": 50
    }

]


def update_mission(user, mission_type, amount=1):

    if user.get("mission_done"):

        return


    if user.get("mission_type") != mission_type:

        return


    user["mission_progress"] += amount


    if user["mission_progress"] >= user["mission_goal"]:

        user["mission_progress"] = user["mission_goal"]

        user["mission_done"] = True

        user["coin"] += user["mission_reward_coin"]

        user["xp"] += user["mission_reward_xp"]


    update_user(user)



def generate_mission(user):

    mission = random.choice(MISSIONS)


    user["mission_type"] = mission["type"]

    user["mission_name"] = mission["name"]

    user["mission_goal"] = mission["goal"]

    user["mission_progress"] = 0

    user["mission_done"] = False

    user["mission_reward_coin"] = mission["reward_coin"]

    user["mission_reward_xp"] = mission["reward_xp"]



def check_daily_mission(user):

    today = int(time.time() // 86400)


    if user.get("mission_day") != today:

        user["mission_day"] = today

        generate_mission(user)

        update_user(user)

        return True


    return False



async def mission(message):

    user = get_user(
        str(message.author.id)
    )


    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return


    check_daily_mission(user)


    update_user(user)


    text = f"""
🎯 چالش روزانه

━━━━━━━━━━━━━━

📌 {user['mission_name']}

📈 پیشرفت:
{user['mission_progress']}/{user['mission_goal']}


🎁 جایزه:

💰 {user['mission_reward_coin']} Coin

✨ {user['mission_reward_xp']} XP

"""


    if user["mission_done"]:

        text += "✅ انجام شده"

    else:

        text += "💪 ادامه بده!"


    await message.reply(text)
