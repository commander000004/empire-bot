from bale import Bot
from config import TOKEN
from router import handle_message

bot = Bot(TOKEN)


@bot.event
async def on_message(message):
    await handle_message(bot, message)


print("=" * 35)
print("🤖 Empire Bot is Online")
print("=" * 35)

bot.run()