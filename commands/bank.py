import random

from bale import Message

from database import (
    get_user_by_bale_id,
    create_user,
    update_user,
    get_user_by_card
)


ACCOUNT_PRICE = 1000
CARD_PRICE = 200


def convert_numbers(text):

    table = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    )

    return text.translate(table)


def account_exists(account):

    from database import load_users

    users = load_users()

    for user in users:

        if user["bank"]["account"] == account:
            return True

    return False



def generate_account():

    while True:

        account = str(
            random.randint(
                1000000000,
                9999999999
            )
        )

        if not account_exists(account):
            return account




def generate_card():

    while True:

        card = "04"

        for _ in range(14):

            card += str(
                random.randint(
                    0,
                    9
                )
            )

        if get_user_by_card(card) is None:
            return card




async def bank_handler(
    bot,
    message: Message
):

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


    text = message.content.strip()



    # ==========================
    # نمایش بانک
    # ==========================

    if text == "بانک":

        bank = user["bank"]


        if bank["account"] is None:

            await bot.send_message(

                message.chat.id,

                "🏦 بانک Empire\n\n"

                "به بانک Empire خوش آمدید.\n\n"

                "❌ شما هنوز حساب بانکی ندارید.\n\n"

                f"💰 هزینه افتتاح حساب : {ACCOUNT_PRICE} Coin\n\n"

                "✏️ دستور:\n"

                "افتتاح حساب"

            )

            return



        if bank["card"] is None:

            await bot.send_message(

                message.chat.id,

                "🏦 بانک Empire\n\n"

                f"📄 شماره حساب : {bank['account']}\n"

                f"💰 موجودی بانک : {bank['balance']} Coin\n\n"

                "💳 شما هنوز کارت بانکی ندارید.\n\n"

                f"💰 هزینه ساخت کارت : {CARD_PRICE} Coin\n\n"

                "✏️ دستور:\n"

                "خریدن کارت"

            )

            return



        await bot.send_message(

            message.chat.id,

            "🏦 بانک Empire\n\n"

            f"👤 {user['name']}\n\n"

            f"💰 موجودی بانک : {bank['balance']} Coin\n"

            f"📄 شماره حساب : {bank['account']}\n"

            f"💳 شماره کارت : {bank['card']}\n"

            f"💵 وام : {bank['loan']} Coin"

        )

        return




    # ==========================
    # افتتاح حساب
    # ==========================

    if text == "افتتاح حساب":

        if user["bank"]["account"] is not None:

            await bot.send_message(

                message.chat.id,

                "❌ شما قبلاً حساب بانکی ساخته‌اید."

            )

            return


        if user["coin"] < ACCOUNT_PRICE:

            await bot.send_message(

                message.chat.id,

                "❌ کوین کافی ندارید."

            )

            return


        user["coin"] -= ACCOUNT_PRICE

        user["bank"]["account"] = generate_account()

        update_user(user)


        await bot.send_message(

            message.chat.id,

            "✅ حساب بانکی شما با موفقیت ساخته شد.\n\n"

            f"📄 شماره حساب:\n{user['bank']['account']}"

        )

        return
        
            # ==========================
    # خرید کارت
    # ==========================

    if text == "خریدن کارت":

        if user["bank"]["account"] is None:

            await bot.send_message(
                message.chat.id,
                "❌ ابتدا باید حساب بانکی افتتاح کنید."
            )

            return


        if user["bank"]["card"] is not None:

            await bot.send_message(
                message.chat.id,
                "❌ شما قبلاً کارت بانکی دریافت کرده‌اید."
            )

            return


        if user["coin"] < CARD_PRICE:

            await bot.send_message(
                message.chat.id,
                "❌ کوین کافی ندارید."
            )

            return


        user["coin"] -= CARD_PRICE

        user["bank"]["card"] = generate_card()

        update_user(user)


        await bot.send_message(

            message.chat.id,

            "💳 کارت بانکی شما صادر شد.\n\n"

            f"شماره کارت:\n"

            f"{user['bank']['card']}"

        )

        return



        # ==========================
    # کارت به کارت
    # ==========================

    if text.startswith("کارت به کارت"):

        args = convert_numbers(text).split()

        if len(args) != 5:

            await bot.send_message(

                message.chat.id,

                "❌ فرمت صحیح:\n\n"

                "کارت به کارت 2000 0412345678901234"

            )

            return


        try:

            amount = int(args[3])

        except:

            await bot.send_message(

                message.chat.id,

                "❌ مبلغ نامعتبر است."

            )

            return


        card = args[4]


        if user["bank"]["card"] is None:

            await bot.send_message(

                message.chat.id,

                "❌ ابتدا کارت بانکی تهیه کنید."

            )

            return


        if amount <= 0:

            await bot.send_message(

                message.chat.id,

                "❌ مبلغ باید بیشتر از صفر باشد."

            )

            return


        if len(card) != 16 or not card.startswith("04"):

            await bot.send_message(

                message.chat.id,

                "❌ شماره کارت نامعتبر است."

            )

            return


        target = get_user_by_card(card)

        if target is None:

            await bot.send_message(

                message.chat.id,

                "❌ کارت مقصد پیدا نشد."

            )

            return


        if target["bale_id"] == user["bale_id"]:

            await bot.send_message(

                message.chat.id,

                "❌ نمی‌توانید به کارت خودتان پول انتقال دهید."

            )

            return


        if user["bank"]["balance"] < amount:

            await bot.send_message(

                message.chat.id,

                "❌ موجودی حساب بانکی شما کافی نیست."

            )

            return


        user["bank"]["balance"] -= amount
        target["bank"]["balance"] += amount

        update_user(user)
        update_user(target)


        await bot.send_message(

            message.chat.id,

            "✅ انتقال با موفقیت انجام شد.\n\n"

            f"💸 مبلغ: {amount:,} Coin\n"

            f"💳 مقصد: {card}"

        )

        return
        
        
        
        
            # ==========================
    # واریز
    # ==========================

    if text.startswith("واریز"):

        args = convert_numbers(text).split()

        if len(args) != 2:

            await bot.send_message(
                message.chat.id,
                "❌ فرمت صحیح:\n\nواریز 5000"
            )

            return

        try:

            amount = int(args[1])

        except:

            await bot.send_message(
                message.chat.id,
                "❌ مبلغ نامعتبر است."
            )

            return

        if amount <= 0:

            await bot.send_message(
                message.chat.id,
                "❌ مبلغ باید بیشتر از صفر باشد."
            )

            return

        if user["coin"] < amount:

            await bot.send_message(
                message.chat.id,
                "❌ کوین کافی ندارید."
            )

            return

        user["coin"] -= amount
        user["bank"]["balance"] += amount

        update_user(user)

        await bot.send_message(

            message.chat.id,

            f"✅ {amount:,} Coin به حساب بانکی شما واریز شد."

        )

        return
        
        
        
        
            # ==========================
    # برداشت
    # ==========================

    if text.startswith("برداشت"):

        args = convert_numbers(text).split()

        if len(args) != 2:

            await bot.send_message(
                message.chat.id,
                "❌ فرمت صحیح:\n\nبرداشت 5000"
            )

            return

        try:

            amount = int(args[1])

        except:

            await bot.send_message(
                message.chat.id,
                "❌ مبلغ نامعتبر است."
            )

            return

        if amount <= 0:

            await bot.send_message(
                message.chat.id,
                "❌ مبلغ باید بیشتر از صفر باشد."
            )

            return

        if user["bank"]["balance"] < amount:

            await bot.send_message(
                message.chat.id,
                "❌ موجودی بانک کافی نیست."
            )

            return

        user["bank"]["balance"] -= amount
        user["coin"] += amount

        update_user(user)

        await bot.send_message(

            message.chat.id,

            f"✅ {amount:,} Coin از حساب بانکی برداشت شد."

        )

        return
        
 