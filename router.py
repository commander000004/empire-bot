# router.py


from commands.profile import profile
from commands.jobs import jobs, choose_job
from commands.work import work

from commands.bank import (
    bank,
    make_card,
    deposit,
    withdraw,
    card_transfer
)

from commands.shop import (
    shop,
    buy,
    inventory
)

from commands.help import help_command

from commands.admin import (
    admin_panel,
    stats,
    set_player,
    ban_user,
    unban_user,
    broadcast
)

from commands.leaderboard import (
    leaderboard,
    leaderboard_level,
    leaderboard_xp,
    leaderboard_gem
)

from database import (
    add_group,
    get_user
)


async def handle_message(message, bot):

    text = message.text.strip()
    
    
        # =====================
    # Ban Check
    # =====================

    user = get_user(
        str(message.author.id)
    )


    if user and user["banned"]:

        await message.reply(
            "🚫 شما از Empire محروم شده‌اید."
        )

        return
        

    # ذخیره گروه
    if message.chat.type != "private":

        try:

            add_group(
                message.chat.id,
                getattr(
                    message.chat,
                    "title",
                    "Unknown"
                )
            )

        except:
            pass

    # فقط گروه
    if message.chat.type == "private":

        await message.reply(

            "🤖 ربات فقط داخل گروه‌ها فعال است.\n\n"
            "➕ لطفاً ربات را به گروه خود اضافه کنید."

        )

        return

    # =====================
    # پنل ادمین
    # =====================

    if text == "پنل":

        await admin_panel(message)
        return

    

        await stats(message)
        return
        
        
        
        
                # =====================
    # پنل ادمین
    # =====================

    if text == "پنل":

        await admin_panel(message)

        return


    if text == "آمار":

        await stats(message)

        return


    # =====================
    # Ban System
    # =====================

    if text.startswith("بن "):

        try:

            user_id = text.split()[1]

            await ban_user(
                message,
                user_id
            )

        except:

            await message.reply(
                "❌ مثال:\nبن 123456"
            )

        return


    if text.startswith("آنبن "):

        try:

            user_id = text.split()[1]

            await unban_user(
                message,
                user_id
            )

        except:

            await message.reply(
                "❌ مثال:\nآنبن 123456"
            )

        return
        
            # =====================
    # Broadcast
    # =====================

    if text.startswith("همگانی "):

        await message.reply(
            "✅ دستور همگانی شناسایی شد"
        )

        msg = text.replace(
            "همگانی ",
            "",
            1
        )

        await broadcast(
            message,
            bot,
            msg
        )

        return
        
         
           
    # =====================
    # پروفایل
    # =====================
    
    
    
    
            # =====================
    # تنظیم بازیکن (Owner)
    # =====================

    if text.startswith("تنظیم "):

        try:

            data = text.split()

            mode = data[1]

            user_id = data[2]

            amount = int(data[3])


            await set_player(
                message,
                mode,
                user_id,
                amount
            )


        except:

            await message.reply(

                "❌ فرمت اشتباه.\n\n"
                "مثال:\n"
                "تنظیم کوین 123456 50000\n"
                "تنظیم جم 123456 100\n"
                "تنظیم xp 123456 5000\n"
                "تنظیم لول 123456 20"

            )


        return

    # =====================
    # پروفایل
    # =====================

    if text in [

        "پروفایل",
        "پروفایل من",
        "پروفایل💳"

    ]:

        await profile(message)
        return

    # =====================
    # راهنما
    # =====================

    if text in [

        "راهنما",
        "help",
        "/help"

    ]:

        await help_command(message)
        return

    # =====================
    # شغل
    # =====================

    if text in [

        "شغل",
        "شغل ها",
        "شغل‌ها"

    ]:

        await jobs(message)
        return

    if text.startswith("انتخاب "):

        job = text.replace(
            "انتخاب ",
            "",
            1
        )

        await choose_job(
            message,
            job
        )

        return

    # =====================
    # کار
    # =====================

    if text == "کار":

        await work(message)

        return

    # =====================
    # بانک
    # =====================

    if text == "بانک":

        await bank(message)

        return

    if text == "ساخت کارت":

        await make_card(message)

        return    # =====================
    # واریز
    # =====================

    if text.startswith("واریز "):

        try:

            amount = int(
                text.split()[1]
            )

            await deposit(
                message,
                amount
            )

        except:

            await message.reply(
                "❌ مثال:\nواریز 1000"
            )

        return

    # =====================
    # برداشت
    # =====================

    if text.startswith("برداشت "):

        try:

            amount = int(
                text.split()[1]
            )

            await withdraw(
                message,
                amount
            )

        except:

            await message.reply(
                "❌ مثال:\nبرداشت 1000"
            )

        return

    # =====================
    # کارت به کارت
    # =====================

    if text.startswith("کارت به کارت "):

        try:

            data = text.split()

            card = data[3]
            amount = int(data[4])

            await card_transfer(
                message,
                card,
                amount
            )

        except:

            await message.reply(
                "❌ مثال:\n"
                "کارت به کارت EMP-123456 1000"
            )

        return

    # =====================
    # فروشگاه
    # =====================

    if text in [

        "فروشگاه",
        "شاپ",
        "shop"

    ]:

        await shop(message)

        return

    # =====================
    # خرید
    # =====================

    if text.startswith("خرید "):

        item = text.replace(
            "خرید ",
            "",
            1
        )

        await buy(
            message,
            item
        )

        return

    # =====================
    # کیف
    # =====================

    if text in [

        "کیف",
        "کوله",
        "inventory",
        "Inventory"

    ]:

        await inventory(message)

        return

    # =====================
    # لیدربورد
    # =====================

    if text == "لیدربورد":

        await leaderboard(message)
        return


    if text == "لیدربورد لول":

        await leaderboard_level(message)
        return


    if text == "لیدربورد XP":

        await leaderboard_xp(message)
        return


    if text == "لیدربورد جم":

        await leaderboard_gem(message)
        return

    # =====================
    # دستور ناشناخته
    # =====================

    # فعلاً هیچ پاسخی نمی‌دهد
    return
        
        
        
        
  