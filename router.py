from commands.start import start_private, start_group
from commands.jobs import select_job
from commands.shop import buy_command
from commands.bank import bank_handler
from commands_map import COMMANDS


async def handle_message(bot, message):

    text = (message.content or "").strip()


    # پیام خصوصی
    if message.chat.type == "private":

        if text == "/start":

            await start_private(
                bot,
                message
            )

        return


    # فقط گروه
    if message.chat.type not in [
        "group",
        "supergroup"
    ]:

        return


    # استارت
    if text == "/start":

        await start_group(
            bot,
            message
        )

        return


    # انتخاب شغل
    if text.startswith("انتخاب شغل "):

        job_name = text.replace(
            "انتخاب شغل ",
            ""
        )

        await select_job(
            bot,
            message,
            job_name
        )

        return


    # خرید آیتم
    if text.startswith("خرید "):

        await buy_command(
            bot,
            message
        )

        return


    # دستورات بانک
    if (
        text == "بانک"
        or text == "افتتاح حساب"
        or text == "خریدن کارت"
        or text.startswith("کارت به کارت")
        or text.startswith("واریز")
        or text.startswith("برداشت")
    ):

        await bank_handler(
            bot,
            message
        )

        return


    # دستورات معمولی
    for handler, names in COMMANDS.items():

        if text in names:

            await handler(
                bot,
                message
            )

            return