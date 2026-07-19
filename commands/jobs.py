import json

from bale import Message

from database import (
    get_user_by_bale_id,
    create_user,
    update_user
)


JOBS_FILE = "data/jobs.json"



def load_jobs():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)





async def jobs_handler(bot, message: Message):

    jobs = load_jobs()


    user = get_user_by_bale_id(
        message.author.id
    )


    if user is None:

        user = create_user(
            message.author.id,
            message.author.first_name
        )



    text = "💼 شغل‌های Empire\n\n"



    for name, info in jobs.items():


        required_level = info["level"]


        if user["level"] >= required_level:

            status = "🟢 باز"

        else:

            status = "🔒 قفل"



        text += (

            f"{status} | {name}\n"

            f"⭐ سطح موردنیاز: {required_level}\n"

        )


        if status == "🔒 قفل":

            text += (

                f"🔓 باز شدن در سطح {required_level}\n"

            )


        text += "\n"




    text += (

        "━━━━━━━━━━━━━━\n"

        "برای انتخاب شغل:\n\n"

        "انتخاب شغل [نام شغل]\n\n"

        "مثال:\n"

        "انتخاب شغل کشاورز"

    )



    await bot.send_message(

        message.chat.id,

        text

    )








async def select_job(bot, message: Message, job_name):


    jobs = load_jobs()


    user = get_user_by_bale_id(
        message.author.id
    )



    if user is None:


        user = create_user(

            message.author.id,

            message.author.first_name

        )





    if job_name not in jobs:


        await bot.send_message(

            message.chat.id,

            "❌ چنین شغلی وجود ندارد."

        )

        return





    job = jobs[job_name]




    if user["level"] < job["level"]:


        await bot.send_message(

            message.chat.id,

            f"🔒 این شغل هنوز باز نشده.\n\n"

            f"💼 شغل: {job_name}\n"

            f"⭐ سطح لازم: {job['level']}\n"

            f"⭐ سطح فعلی شما: {user['level']}"

        )

        return





    user["job"] = job_name


    update_user(user)



    await bot.send_message(

        message.chat.id,


        f"✅ شغل انتخاب شد!\n\n"

        f"💼 شغل فعلی:\n"

        f"{job_name}"

    )