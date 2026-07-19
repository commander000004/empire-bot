from bale import Message

from database import (
    get_user_by_bale_id,
    create_user
)



def get_needed_xp(level):

    return level * 100




async def profile_handler(bot, message: Message):

    bale_id = message.author.id

    name = message.author.first_name


    user = get_user_by_bale_id(
        bale_id
    )


    if user is None:

        user = create_user(
            bale_id,
            name
        )



    job = user.get(
        "job"
    )


    if job is None:

        job = "ندارد"



    inventory = user.get(
        "inventory",
        []
    )


    needed_xp = get_needed_xp(
        user["level"]
    )



    text = (

        "👤 پروفایل Empire\n\n"

        f"🆔 ID : {user['game_id']}\n"

        f"👤 نام : {user['name']}\n\n"

        f"⭐ سطح : {user['level']}\n"

        f"✨ XP : {user['xp']}/{needed_xp}\n\n"

        f"💰 کوین : {user['coin']}\n"

        f"💎 جم : {user['gem']}\n\n"

        f"💼 شغل : {job}\n\n"

        f"🎒 تعداد آیتم‌ها : {len(inventory)}\n\n"

        f"🏦 بانک : {user['bank']}"

    )



    await bot.send_message(

        message.chat.id,

        text

    )