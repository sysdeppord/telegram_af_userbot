from pyrogram import Client, filters, idle
from tg_config import api_id, api_hash, bot_token
from db_engine import Setting
from user_processor import UserMessages
from bot_processor import Sorter

account = "test000"
u_id = 0
user = Client(name=account, api_id=api_id, api_hash=api_hash)
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
setting = Setting()
setting.load_all()


def check_my_id():
    """
    Check user telegram ID. Need on first run bot.
    """
    me = user.get_me()
    my_id = me.id
    if my_id == setting.my_id:
        pass
    else:
        setting.add_my_id(my_id)


@user.on_message(filters.private & ~filters.bot)
async def user_message(client, message):
    processor = UserMessages()
    await processor.forward_logic(user, message, setting)


@bot.on_callback_query()
async def bot_callback_query(client, callbackdata):
    processor = Sorter()
    await processor.callback_filter(bot, user, callbackdata, setting)


@bot.on_message(filters.private & ~filters.me)
async def bot_message(client, message):
    processor = Sorter()
    await processor.message_filter(bot, user, message, setting)


if __name__ == '__main__':
    print('Connecting to telegram account... Please wait...')
    user.start()
    print("Connected!")
    check_my_id()
    print('Connecting to control panel... Please wait...')
    bot.start()
    print("Connected!")
    idle()
    user.stop()
    bot.stop()
