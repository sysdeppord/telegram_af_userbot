# import os
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from cp_bot.bot_processor import Sorter
from handlers.handlers import UserHandlers
from config.app_config import *
from config.tg_config import *
from proxy_class import setting

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, workdir="./files/bot")

users = {}


def add_user_client():
    print("Building users apps")
    for usr in setting.user_setting:
        if setting.user_setting[f"{usr}"]["authorised"] and os.path.exists(f"./files/users/u{usr}") and setting.user_setting[f"{usr}"]["is_blocked"] != 1:
            user_id = usr
            name = f"u{user_id}"
            users[user_id] = Client(name, api_id=api_id, api_hash=api_hash, app_version=name_app + ver_app,
                                      device_model=device_model, system_version=system_version,
                                      workdir=f"./files/users/{name}")
    print("OK")


def check_and_create_folders():
    if not os.path.exists("./files"):
        os.mkdir("./files")
    if not os.path.exists("./files/bot"):
        os.mkdir("./files/bot")
    if not os.path.exists("./files/users"):
        os.mkdir("./files/users")


@bot.on_callback_query()
async def bot_callback_query(client, callback_data):
    processor = Sorter(client, users, callback_data=callback_data)
    await processor.callback_filter()


@bot.on_message(filters.private & ~filters.me) # old
async def bot_message(client, message):
    processor = Sorter(client, users, message=message)
    await processor.message_filter()

user_handlers = UserHandlers(bot)
user_message = user_handlers.user_message

if __name__ == "__main__":
    add_user_client()
    check_and_create_folders()
    print("Starting control panel")
    bot.start()
    bot_client = bot
    print("OK")
    print("Trying to run user apps if exist")
    for app in users:
        # Add a MessageHandler to each Client and start it
        users[app].add_handler(MessageHandler(user_message))
        print(f"Running {users[app].name}")
        users[app].start()
        print("OK")
    idle()
    bot.stop()
    for app in users:
        print(f"Stopping {users[app].name}")
        try:
            users[app].stop()
        except:
            print(f"Already stopped {users[app].name}")
