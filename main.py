from bale import Bot
from config import TOKEN

from database import init_db
from router import handle_message

# اول دیتابیس ساخته بشه
init_db()

bot = Bot(token=TOKEN)


@bot.event
async def on_ready():
    print("Empire Bot Started 🚀")


@bot.event
async def on_message(message):
    await handle_message(
        message,
        bot
    )


bot.run()