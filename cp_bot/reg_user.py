from pyrogram import Client
from pyrogram.errors import (PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded,
                             PasswordHashInvalid, FloodWait, PhonePasswordFlood)
from pyrogram.handlers import MessageHandler
from handlers.handlers import UserHandlers
from pyrogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from proxy_class import setting
from cp_bot.user_auth import UserAuth
from config.tg_config import *
from config.app_config import *
from cp_bot import keyboards


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

    async def auth_number(self, user_id, message, client):
        if message.contact:
            text = "Немного подожди..."
            reply_markup = ReplyKeyboardRemove()
            await client.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
            phone_number = message.contact.phone_number
            if phone_number.isdigit():
                auth = UserAuth()
                try:
                    await auth.create_app(user_id, phone_number)
                    text = ("Отлично!\nТеперь введи код авторизации, который отправил телеграмм используя клавиатуру "
                            "снизу.")
                    keyboard = keyboards.enter_code
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await client.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
                    setting.user_setting[f"{user_id}"]['menu_point'] = "send_code"
                except PhoneNumberInvalid:
                    await message.reply_text("Ты отправил не действительный номер телефона!\n"
                                             "Перепроверь и попробуй ещё раз!")
                except PhonePasswordFlood:
                    await message.reply_text("У тебя было слишком много попыток входа! Приходи позже!")
                    setting.user_setting[f"{user_id}"]['menu_point'] = ""
                except FloodWait as time:
                    await message.reply_text(f"У тебя было слишком много попыток входа! Приходи позже!")
                    setting.user_setting[f"{user_id}"]['menu_point'] = ""

            else:
                await message.reply_text("Ты отправил не номер телефона! Попробуй ещё раз!")


    async def input_auth_code(self, callback_data, user_id, users, client):
        message_id = callback_data.message.id
        chat_id = callback_data.from_user.id
        data = callback_data.data.replace("code_", "")
        if data.isdigit():
            if len(setting.user_setting[f"{user_id}"]['auth_code']) < 5:
                setting.user_setting[f"{user_id}"]['auth_code'] += data
                code = setting.user_setting[f"{user_id}"]['auth_code']
                text = (f"Теперь введи код авторизации, который отправил телеграмм используя клавиатуру снизу.\n\n"
                        f"Введённый тобой код: \"**{code}**\"")
                keyboard = keyboards.enter_code
                reply_markup = InlineKeyboardMarkup(keyboard)
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                               reply_markup=reply_markup)
            if len(setting.user_setting[f"{user_id}"]['auth_code']) >= 5:
                code = setting.user_setting[f"{user_id}"]['auth_code']
                text = (f"Введено 5 из 5 символов кода авторизации! Если код не правильный - используй кнопку стереть"
                        f"\n\nВведённый тобой код: \"**{code}**\"")
                keyboard = keyboards.enter_code
                reply_markup = InlineKeyboardMarkup(keyboard)
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                               reply_markup=reply_markup)
        elif data == "ok":
            await self.send_code(callback_data, user_id, users, client)
        elif data == "remove":
            setting.user_setting[f"{user_id}"]['auth_code'] = setting.user_setting[f"{user_id}"]['auth_code'][:-1]
            code = setting.user_setting[f"{user_id}"]['auth_code']
            text = (f"Теперь введи код авторизации, который отправил телеграмм используя клавиатуру снизу.\n\n"
                    f"Введённый тобой код: \"**{code}**\"")
            keyboard = keyboards.enter_code
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                           reply_markup=reply_markup)

    async def filter(self, message, users, client):
        user_id = message.from_user.id
        if not setting.user_setting.get(f"{user_id}"):
            setting.register(user_id)
        if not setting.user_setting[f"{user_id}"]['authorised'] and setting.user_setting[f"{user_id}"]['menu_point'] == "":
            text = ("Ты не зарегистрирован! Чтобы продолжить отправь мне свой номер телефона контактом с помощью "
                    "клавиатуры внизу\n\n**ВАЖНО!!! Авторизация со включённым облачным паролем может работать "
                    "некорректно! На время авторизации его лучше отключить! После успешной авторизации можешь вернуть "
                    "его назад.**")
            button = KeyboardButton(text="Отправить контакт", request_contact=True)
            keyboard = [[button]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True,
                                               is_persistent=True)
            await client.send_message(text=text, chat_id=user_id, reply_markup=reply_markup)
            setting.user_setting[f"{user_id}"]['menu_point'] = "auth_number"
        elif setting.user_setting[f"{user_id}"]['menu_point'] == "auth_number":
            await self.auth_number(user_id, message, client)
        #elif setting.user_setting[f"{user_id}"]['menu_point'] == "send_code":
        #    await self.send_code(message, user_id, users, client)
        elif setting.user_setting[f"{user_id}"]['menu_point'] == "cloud_password":
            await self.check_password(message, user_id, users, client)

    async def check_password(self, message, user_id, users, client):
        password = message.text
        auth = UserAuth()
        try:
            await auth.check_cloud_password(user_id, password)
            await auth.remove_user_app(user_id)
            await message.reply_text("Авторизация бота прошла успешно!\nВнесение данных в базу аккаунтов и "
                                     "запуск бота, подожди немного...")
            setting.authorise(user_id)
            await self.run_userbot(user_id, users, client)
            text = ("Ты авторизовался в боте!\nЧтобы бот пересылал сообщения не забудь запустить его в"
                    " настройках. Приятного пользования!")
            keyboard = keyboards.auth_ok
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
            setting.user_setting[f"{user_id}"]["menu_point"] = ""
        except PasswordHashInvalid:
            text = "Пароль 2х факторной авторизации был введён не правильно!\nПересмотри и введи правильно!"
            hint = await auth.check_hint_cloud_password(user_id)
            if hint:
                text += f"\nПодсказка к паролю: \"{hint}\""
            setting.user_setting[f"{user_id}"]["menu_point"] = "cloud_password"
            await client.send_message(chat_id=user_id, text=text)
        except FloodWait as time:
            text = (f"Ты сильно часто вводил неправильный пароль!\nТелеграм заморозил попытки входа на {time} секунд.\n"
                    f"Мы сбросили данные авторизации, возвращайся когда пройдёт это время и снова запусти /start")
            setting.user_setting[f"{user_id}"]["menu_point"] = ""
            await client.send_message(chat_id=user_id, text=text)
        except AttributeError:
            text = (f"Ты измения пароль во время авторизации?! Помянем!\nМы сбросили данные авторизации, и пройди "
                    f"авторизацию с нуля! /start")
            setting.user_setting[f"{user_id}"]["menu_point"] = ""
            await client.send_message(chat_id=user_id, text=text)




    async def send_code(self, callback_data, user_id, users, client):
        message_id = callback_data.message.id
        chat_id = callback_data.from_user.id
        code = setting.user_setting[f"{user_id}"]['auth_code']
        auth = UserAuth()
        try:
            await auth.auth_code(user_id, code, client)
            if setting.user_setting[f"{user_id}"]["temp_data"] == "not_self_id":
                text = ("Ты вошел не в свой аккаунт! Авторизация отменена!\nХазяину аккаунта отправлено"
                        " сообщение о попытке входа!")
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                       reply_markup="")
                await auth.remove_user_app(user_id)
            else:
                await auth.remove_user_app(user_id)
                text = ("Авторизация бота прошла успешно!\nВнесение данных в базу аккаунтов и запуск бота, "
                        "подожди немного...")
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                               reply_markup="")
                setting.authorise(user_id)
                await self.run_userbot(user_id, users, client)
                text = ("Ты авторизовался в боте!\nЧтобы бот пересылал сообщения не забудь запустить его в"
                        " настройках. Приятного пользования!")
                keyboard = keyboards.auth_ok
                reply_markup = InlineKeyboardMarkup(keyboard)
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                               reply_markup=reply_markup)
                setting.user_setting[f"{user_id}"]["menu_point"] = ""
        except PhoneCodeInvalid:
            code = setting.user_setting[f"{user_id}"]['auth_code']
            text = f"Введённый тобой код: \"**{code}**\" - НЕ ПРАВИЛЬНЫЙ!\nПопробуй ещё раз!"
            setting.user_setting[f"{user_id}"]['auth_code'] = ""
            keyboard = keyboards.enter_code
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                           reply_markup=reply_markup)
        except PhoneCodeExpired:
            text = "Срок действия введённого кода истёк.\nПробуем получить ещё один код..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            await auth.resend_code(user_id)
            setting.user_setting[f"{user_id}"]['auth_code'] = ""
            text = "Код отправлен ещё раз!\nПопробуй ввести его снова"
            keyboard = keyboards.enter_code
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                           reply_markup=reply_markup)
        except SessionPasswordNeeded:
            text = "Теперь необходимо ввести пароль 2х факторной авторизации!"
            hint = await auth.check_hint_cloud_password(user_id)
            if hint:
                text += f"\nПодсказка к паролю: \"{hint}\""
            setting.user_setting[f"{user_id}"]["menu_point"] = "cloud_password"
            await client.send_message(chat_id=chat_id, text=text)
        except FloodWait as time:
            text = (f"Ты ввёл слишком много раз неправильный код авторизации и телеграм заморозил все попытки входа!\n"
                    f"Ограничение снимется через \"{time}\" секунд.\nМы сбросили данные авторизации, возвращайся "
                    f"когда пройдёт это время и снова запусти /start")
            setting.user_setting[f"{user_id}"]["menu_point"] = ""
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")

    @staticmethod
    async def run_userbot(user_id, users, client):
        user_handlers = UserHandlers(client)
        user_message = user_handlers.user_message
        name = f"u{user_id}"
        users.append(Client(name, api_id=api_id, api_hash=api_hash, app_version=name_app+ver_app,
                     device_model=device_model, system_version=system_version, workdir=f"./files/users/{name}"))
        for user in users:
            if user.name == name:
                user.add_handler(MessageHandler(user_message))
                await user.start()
