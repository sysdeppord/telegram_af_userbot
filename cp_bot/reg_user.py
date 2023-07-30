from pyrogram import Client
from pyrogram.handlers import MessageHandler
from handlers.handlers import UserHandlers
from proxy_class import setting
from cp_bot.user_auth import UserAuth
from config.tg_config import *




class NotRegistered:

    @staticmethod
    async def only_digit(phone_number):
        """Need to remove phone code symbols like as +, -, (, ), 'spaces'. Add another if need other"""
        phone_number = phone_number.replace("+", "")
        phone_number = phone_number.replace("-", "")
        phone_number = phone_number.replace(" ", "")
        phone_number = phone_number.replace("(", "")
        phone_number = phone_number.replace(")", "")
        return phone_number

    async def auth_number(self, user_id, message):
        phone_number = await self.only_digit(message.text)
        if phone_number.isdigit():
            auth = UserAuth()
            await auth.create_app(user_id, phone_number)
            await message.reply_text(
                "DONE!\nТеперь отправь код авторизации, с цифрами через пробел (прим. \"1 2 266\" и подобное)")
            setting.user_setting[f"{user_id}"]['menu_point'] = "send_code"
        else:
            await message.reply_text("Ты отправил не номер телефона! Попробуй ещё раз!")

    async def filter(self, message, users, client):
        user_id = message.from_user.id
        if not setting.user_setting.get(f"{user_id}"):
            setting.register(user_id)
        if not setting.user_setting[f"{user_id}"]['authorised'] and setting.user_setting[f"{user_id}"]['menu_point'] == "":
            await message.reply_text("Ты не зарегистрирован! Чтобы продолжить отправь мне свой номер телефона в "
                                     "международном формате (+380990000000)\n\n**ВАЖНО!!! авторизация со включённым "
                                     "облачным паролем НЕДОСТУПНА!!! И НЕ БУДЕТ ДОСТУПНА!!!\nНа время авторизации его"
                                     " прийдётся отключить! После успешной авторизации можешь вернуть его назад.**")
            setting.user_setting[f"{user_id}"]['menu_point'] = "auth_number"
        elif setting.user_setting[f"{user_id}"]['menu_point'] == "auth_number":
            await self.auth_number(user_id, message)
        elif setting.user_setting[f"{user_id}"]['menu_point'] == "send_code":
            await self.send_code(message, user_id, users, client)

    async def send_code(self, message, user_id, users, client):
        v_dig = message.text
        v_dig = v_dig.replace(" ", "")
        if v_dig.isdigit():
            if len(v_dig) == 5:
                code = v_dig
                auth = UserAuth()
                await auth.auth_code(user_id, code, client)
                # print(setting.user_setting)
                if setting.user_setting[f"{user_id}"]["temp_data"] == "not_self_id":
                    await message.reply_text("Ты вошел не в свой аккаунт! Авторизация отменена!\nХазяину аккаунта "
                                             "отправлено сообщение о попытке входа!")
                else:
                    await message.reply_text("Авторизация бота прошла успешно!\n"
                                         "Внесение данных в базу аккаунтов и запуск бота, подожди немного...")
                    setting.authorise(user_id)
                    await self.run_userbot(user_id, users, client)
                    await message.reply_text("Бот запущен!\nПриятного пользования!\nНажми ещё раз /start)")
            else:
                await message.reply_text(f"Код авторизации не содержит 5 цифр, количество цифр в твоём коде "
                                         f"\"{len(v_dig)}\"\nПопробуй ввести код ещё раз!")
        else:
            await message.reply_text("Код авторизации неправильный, попробуй ещё раз!")

    @staticmethod
    async def run_userbot(user_id, users, client):
        user_handlers = UserHandlers(client)
        user_message = user_handlers.user_message
        name = f"u{user_id}"
        users.append(Client(name, api_id=api_id, api_hash=api_hash))
        for user in users:
            if user.name == name:
                user.add_handler(MessageHandler(user_message))
                await user.start()
