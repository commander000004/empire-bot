# commands/profile.py

from database import (
    get_user,
    create_user
)

from level import xp_need
from unlocks import get_unlocked_jobs


async def profile(message):

    user_id = str(message.author.id)

    user = get_user(user_id)


    if not user:

        create_user(
            user_id,
            message.author.first_name
        )

        user = get_user(user_id)


    jobs = get_unlocked_jobs(
        user["level"]
    )


    jobs_text = ""

    for job in jobs:

        jobs_text += f"🔓 {job}\n"


    text = f"""
👤 پروفایل

━━━━━━━━━━━━━━

━━━━━━━━━━━━━━

🆔 ID: {user['bale_id']}

نام: {user['name']}

💰 Coin: {user['coin']:,}

💎 Gem: {user['gem']}

⭐ Level: {user['level']}

✨ XP:
{user['xp']}/{xp_need(user['level'])}

━━━━━━━━━━━━━━

👷 شغل فعلی:

{user['job'] if user['job'] else "❌ ندارد"}

━━━━━━━━━━━━━━

🔓 شغل‌های باز شده:

{jobs_text}
"""


    await message.reply(text)