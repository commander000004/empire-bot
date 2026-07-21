async def help_command(message):

    text = """
📖 راهنمای Empire

━━━━━━━━━━━━━━

🌟 شروع بازی

برای شروع ابتدا پروفایل خود را بسازید.

با داشتن پروفایل می‌توانید:
💰 Coin دریافت کنید
✨ Level بالا ببرید
💎 Gem جمع کنید
🏢 در اقتصاد Empire فعالیت کنید

━━━━━━━━━━━━━━

(ادامه متن خودت همینجا)
"""

    await message.bot.send_message(
        message.author.id,
        text
    )
