import random
import time

from database import (
    get_user,
    update_user
)


MISSIONS = [

    {
        "type": "work",
        "name": "۵ بار کار کن",
        "goal": 5,
        "reward_coin": 1500,
        "reward_xp": 30
    },

    {
        "type": "work",
        "name": "۱۰ بار کار کن",
        "goal": 10,
        "reward_coin": 3500,
        "reward_xp": 60
    },

    {
        "type": "work",
        "name": "۱۵ بار کار کن",
        "goal": 15,
        "reward_coin": 6000,
        "reward_xp": 100
    },

    {
        "type": "xp",
        "name": "۵۰ XP کسب کن",
        "goal": 50,
        "reward_coin": 2000,
        "reward_xp": 40
    },

    {
        "type": "coin",
        "name": "۵۰۰۰ Coin کسب کن",
        "goal": 5000,
        "reward_coin": 2500,
        "reward_xp": 50
    },

    {
        "type": "buy",
        "name": "۱ آیتم خریداری کن",
        "goal": 1,
        "reward_coin": 1500,
        "reward_xp": 30
    }

]



def create_mission(user):

    mission = random.choice(MISSIONS)


    user["mission_type"] = mission["type"]

    user["mission_name"] = mission["name"]

    user["mission_goal"] = mission["goal"]

    user["mission_progress"] = 0

    user["mission_done"] = False


    user["mission_reward_coin"] = mission["reward_coin"]

    user["mission_reward_xp"] = mission["reward_xp"]



    user["mission_day"] = int(
        time.time() // 86400
    )





def check_mission(user):

    today = int(
        time.time() // 86400
    )


    if user.get("mission_day") != today:

        create_mission(user)

        return True


    return False





print("MISSIONS UPDATED")
def update_mission(user, mission_type, amount=1):


    if user.get("mission_done"):

        return



    if user.get("mission_type") != mission_type:

        return



    user["mission_progress"] += amount



    if user["mission_progress"] >= user["mission_goal"]:


        user["mission_progress"] = user["mission_goal"]

        user["mission_done"] = True



        user["coin"] += (
            user["mission_reward_coin"]
        )


        user["xp"] += (
            user["mission_reward_xp"]
        )





async def mission(message):


    user = get_user(
        str(message.author.id)
    )


    if not user:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return



    new = check_mission(user)


    if new:

        update_user(user)



    text = (

        "🎯 چالش روزانه Empire\n\n"

        f"📌 {user['mission_name']}\n\n"

        f"📈 پیشرفت: "
        f"{user['mission_progress']}/"
        f"{user['mission_goal']}\n\n"

        "🎁 جایزه:\n"

        f"💰 {user['mission_reward_coin']} Coin\n"

        f"✨ {user['mission_reward_xp']} XP\n\n"

    )


    if user["mission_done"]:

        text += (
            "✅ ماموریت کامل شده و جایزه دریافت شد."
        )

    else:

        text += (
            "💪 ادامه بده تا کامل شود."
        )



    await message.reply(text)
