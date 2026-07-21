import time

from database import (
    get_user,
    create_user
)

from level import xp_need
from unlocks import get_unlocked_jobs


async def profile(message):

    # اگر ریپلای بود، پروفایل شخص ریپلای‌شده را نمایش بده
    if (
        getattr(message, "reply_to_message", None)
        and getattr(message.reply_to_message, "author", None)
    ):
        target = message.reply_to_message.author
    else:
        target = message.author

    user_id = str(target.id)

    user = get_user(user_id)

    if not user:

        create_user(
            user_id,
            target.first_name
        )

        user = get_user(user_id)

    jobs = get_unlocked_jobs(
        user["level"]
    )

    jobs_text = ""

    for job in jobs:
        jobs_text += f"🔓 {job}\n"

    now = int(time.time())

    boosters = ""

    if user["time_booster_until"] > now:

        remain = user["time_booster_until"] - now

        hours = remain // 3600
        minutes = (remain % 3600) // 60

        boosters += (
            f"⏳ تایم بوستر: "
            f"{hours} ساعت "
            f"{minutes} دقیقه\n"
        )

    if user["double_rewards_until"] > now:

        remain = user["double_rewards_until"] - now

        hours = remain // 3600
        minutes = (remain % 3600) // 60

        boosters += (
            f"💰 دابل ریوارد: "
            f"{hours} ساعت "
            f"{minutes} دقیقه\n"
        )

    if boosters == "":
        boosters = "❌ هیچ بوستری فعال نیست."

    current_job = user["job"] if user["job"] else "❌ ندارد"

    text = f"""
👤 پروفایل بازیکن

━━━━━━━━━━━━━━

🆔 آیدی عددی:
{user["bale_id"]}

👤 نام:
{user["name"]}

━━━━━━━━━━━━━━

💰 Coin:
{user["coin"]:,}

💎 Gem:
{user["gem"]}

━━━━━━━━━━━━━━

⭐ Level:
{user["level"]}

✨ XP:
{user["xp"]}/{xp_need(user["level"])}

━━━━━━━━━━━━━━

👷 شغل فعلی:
{current_job}

━━━━━━━━━━━━━━

🚀 بوسترها:

{boosters}

━━━━━━━━━━━━━━

🔓 شغل‌های باز شده:

{jobs_text}
"""

    await message.reply(text)
