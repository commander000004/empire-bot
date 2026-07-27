# commands/transfer.py

from database import get_user, update_user


TRANSFER_TAX = 0.05  # 5%


async def transfer_coin(message, amount):

    # بررسی ریپلای
    reply = getattr(message, "reply_to_message", None)

    if not reply or not getattr(reply, "author", None):

        await message.reply(
            "❌ ابتدا روی پیام کاربری که می‌خواهید به او Coin بدهید ریپلای کنید.\n\n"
            "فرمت صحیح:\n"
            "انتقال کوین عدد\n\n"
            "مثال:\n"
            "انتقال کوین 5000"
        )

        return


    sender_id = str(message.author.id)

    receiver_id = str(reply.author.id)


    # انتقال به خود
    if sender_id == receiver_id:

        await message.reply(
            "❌ نمی‌توانی به خودت Coin انتقال بدهی."
        )

        return


    sender = get_user(sender_id)
    receiver = get_user(receiver_id)


    if not sender:

        await message.reply(
            "❌ ابتدا پروفایل بساز."
        )

        return


    if not receiver:

        await message.reply(
            "❌ گیرنده هنوز در Empire ثبت نشده است."
        )

        return


    # مبلغ
    if amount <= 0:

        await message.reply(
            "❌ مقدار انتقال باید بیشتر از صفر باشد."
        )

        return


    tax = int(amount * TRANSFER_TAX)

    total = amount + tax


    if sender["coin"] < total:

        await message.reply(
            f"❌ Coin کافی نداری.\n\n"
            f"💰 نیاز: {total:,}\n"
            f"💰 موجودی: {sender['coin']:,}"
        )

        return


    sender["coin"] -= total
    receiver["coin"] += amount


    update_user(sender)
    update_user(receiver)


    await message.reply(
        f"✅ انتقال انجام شد.\n\n"
        f"👤 گیرنده:\n"
        f"{receiver['name']}\n\n"
        f"💰 مقدار:\n"
        f"{amount:,} Coin\n\n"
        f"💸 کارمزد:\n"
        f"{tax:,} Coin"
    )


    try:

        await reply.reply(
            f"🎁 Coin دریافت کردی!\n\n"
            f"💰 مقدار:\n"
            f"{amount:,} Coin\n\n"
            f"📤 ارسال کننده:\n"
            f"{sender['name']}"
        )

    except:

        pass
