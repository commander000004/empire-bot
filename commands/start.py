from bale import Message


async def start_private(bot, message: Message):
    text = (
        "👋 سلام، خوش اومدی!\n\n"
        "🏰 این ربات برای استفاده در گروه‌ها ساخته شده است.\n\n"
        "➕ لطفاً ربات را به گروه خود اضافه کنید.\n\n"
        "📖 سپس در گروه دستور زیر را ارسال کنید:\n\n"
        "راهنما"
    )

    await bot.send_message(
        message.chat.id,
        text
    )


async def start_group(bot, message: Message):
    text = (
        "✅ ربات با موفقیت فعال است.\n\n"
        "برای شروع، دستور زیر را ارسال کنید:\n\n"
        "راهنما"
    )

    await bot.send_message(
        message.chat.id,
        text
    )