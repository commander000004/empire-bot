from commands.bank import bank_handler
from commands.help import help_handler
from commands.profile import profile_handler
from commands.jobs import jobs_handler
from commands.work import work_handler
from commands.inventory import inventory_handler
from commands.shop import shop_handler



COMMANDS = {


    help_handler: [

        "راهنما",
        "کمک",
        "راهنمای ربات",

    ],



    profile_handler: [

        "پروفایل",
        "پروفایل من",
        "پروفایل خودم",
        "لول",
        "لول من",
        "سطح",
        "سطح من",

    ],



    jobs_handler: [

        "شغل‌ها",
        "شغل ها",
        "شغل",
        "کارها",
        "کار ها",

    ],



    work_handler: [

        "کار",
        "کارکردن",
        "کار کردن",
        "کار کن",

    ],



    inventory_handler: [

        "کیف",
        "کیف من",
        "آیتم ها",
        "آیتم‌ها",
        "وسایل من",

    ],



    shop_handler: [

        "فروشگاه",
        "فروشگاه آیتم",
        "آیتم شاپ",
        "ایتم شاپ",

    ],
    
    

    bank_handler: [

    "بانک",
    "حساب",
    "حساب بانکی",
    "افتتاح حساب",
    "خریدن کارت"

],



}