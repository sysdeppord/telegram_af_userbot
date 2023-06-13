import copy
import time
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keyboards
from tg_config import api_id, api_hash, name_app, ver_app, system_version, device_model, admin_id
from tg_config import setting
from handlers import user_message

apps = []
release_note = "**СВЕРШИЛОСЬ!**\n" \
               "- Теперь в боте появилась внутренняя авторизация, без танцев с бубном в терминале. Авторизация " \
               "доступна только для аккаунтов с выключеным облачным паролем!\n" \
               "То есть это полноценный мультиаккаунт! Главное внимательно читать инструкцию по каждому шагу...\n" \
               "- Возможно добавлены новые баги..."
about = f"{name_app} - {ver_app}\nPowered by {device_model}"


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

    async def filter(self, message, users):
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
            await self.send_code(message, user_id, users)

    async def send_code(self, message, user_id, users):
        v_dig = message.text
        v_dig = v_dig.replace(" ", "")
        if v_dig.isdigit():
            if len(v_dig) == 5:
                code = v_dig
                auth = UserAuth()
                await auth.auth_code(user_id, code)
                await message.reply_text("Авторизация бота прошла успешно!\n"
                                         "Внесение данных в базу аккаунтов и запуск бота, подожди немного...")
                setting.authorise(user_id)
                await self.run_userbot(user_id, users)
                await message.reply_text("Бот запущен!\nПриятного пользования!\nНажми ещё раз /start)")
            else:
                await message.reply_text(f"Код авторизации не содержит 5 цифр, количество цифр в твоём коде "
                                         f"\"{len(v_dig)}\"\nПопробуй ввести код ещё раз!")
        else:
            await message.reply_text("Код авторизации неправильный, попробуй ещё раз!")

    @staticmethod
    async def run_userbot(user_id, users):
        name = f"u{user_id}"
        users.append(Client(name, api_id=api_id, api_hash=api_hash))
        for user in users:
            if user.name == name:
                user.add_handler(MessageHandler(user_message))
                await user.start()


class Sorter:
    def __init__(self, client, users, message=None, callback_data=None):
        self.message = message
        self.callback_data = callback_data
        if message:
            self.user_id = message.from_user.id
        if callback_data:
            self.user_id = callback_data.from_user.id
        self.processor = Processor(client, message, users, callback_data)
        self.client = client
        self.users = users

    async def callback_filter(self):
        data = self.callback_data.data
        user_app = await GetInfo().get_user_app(self.user_id, self.users)
        if data == "setting":
            await self.processor.setting()
        elif data == "start":
            await self.processor.start()
        elif data == "stop":
            await self.processor.stop()
        elif data == "add":
            await self.processor.add()
        elif data == "remove_step1":
            await self.processor.remove_step1(user_app)
        elif data == "freeze_step1":
            await self.processor.freeze_step1(user_app)
        elif data == "unfreeze_step1":
            await self.processor.unfreeze_step1(user_app)
        elif data == "forward_my_step1":
            await self.processor.forward_my_step1(user_app)
        elif data == "change_destination_step1":
            await self.processor.change_destination_step1(user_app)
        elif data == "main_menu":
            await self.processor.main_menu()
        elif data == "about":
            await self.processor.about()
        elif data == "status":
            await self.processor.status()
        elif data == "list":
            await self.processor.list(user_app)
        elif data == "help":
            await self.processor.help()
        elif data.startswith("select_existing_"):
            await self.processor.destination_select_existing_step2(user_app)
        elif data.startswith("remove_"):
            await self.processor.remove_step2(user_app)
        elif data.startswith("freeze_"):
            await self.processor.freeze_step2(user_app)
        elif data.startswith("unfreeze_"):
            await self.processor.unfreeze_step2(user_app)
        elif data.startswith("change_destination_"):
            await self.processor.change_destination_step2(user_app)
        elif data.startswith("exist_chat_"):
            await self.processor.add_from_exist_chat_step2(user_app)
        elif data.startswith("sync_contact_"):
            await self.processor.add_from_sync_contact_step2(user_app)
        elif data.startswith("forward_my_step2_"):
            await self.processor.forward_my_step2(user_app)
        elif data == "add_from_send_contact_step1":
            await self.processor.add_from_send_contact_step1()
        elif data == "add_from_exist_chat_step1":
            await self.processor.add_from_exist_chat_step1(user_app)
        elif data == "add_from_sync_contact_step1":
            await self.processor.add_from_sync_contact_step1(user_app)
        elif data == "add_from_forwarded_message_step1":
            await self.processor.add_from_forwarded_message_step1()
        elif data == "destination_create_new":
            await self.processor.destination_create_new(user_app)
        elif data == "destination_select_existing_step1":
            await self.processor.destination_select_existing_step1(user_app)
        elif data == "burn_all":
            await self.processor.burn_all()
        elif data == "fbi_open_up":
            await self.processor.fbi_open_up(user_app)
        elif data == "forward_my_off":
            await self.processor.forward_my_off()
        elif data == "forward_my_on":
            await self.processor.forward_my_on()

    async def message_filter(self):
        get_info = GetInfo()
        user = await get_info.get_user_app(self.user_id, self.users)
        if await get_info.is_register(self.user_id):
            if self.message.text == "/start":
                await self.processor.start_message()
            if setting.user_setting[f"{self.user_id}"]["menu_point"] == "add_from_send_contact_step2":
                await self.processor.add_from_send_contact_step2(user)
            if setting.user_setting[f"{self.user_id}"]["menu_point"] == "add_from_forwarded_message_step2":
                await self.processor.add_from_forwarded_message_step2(user)
            if self.message.text == "/upd_start":
                await self.processor.upd_start()
            if self.message.text == "/upd_end":
                await self.processor.upd_end()
        elif not await get_info.is_register(self.user_id):
            not_registered = NotRegistered()
            await not_registered.filter(self.message, self.users)


class Processor:  # fixme додавання блядських пересиланні, методи в БД

    def __init__(self, client, message, users, callback_data):
        self.client = client
        self.message = message
        self.users = users
        self.callback_data = callback_data
        if callback_data:
            self.message_id = callback_data.message.id
            self.chat_id = callback_data.from_user.id
        if message:
            self.chat_id = message.chat.id

    async def start_message(self):  # TODO
        text = "Привет!\nЭто бот для автоматической пересылки!\nДля навигации по меню используй кнопки ниже!"
        keyboard = keyboards.start_message
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = ""
        await self.message.reply_text(text, reply_markup=reply_markup)

    async def main_menu(self):  # TODO
        text = "Привет!\nЭто бот для автоматической пересылки!\nДля навигации по меню используй кнопки ниже!"
        keyboard = keyboards.start_message
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = ""
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add(self):
        text = "Выбери как добавить пользователя:\n\n**Отправлю контакт пользователя** - Нужно зайти в чат с " \
               "пользователем, нажать **поделиться** и отправить контакт боту.\n**Выберу чат с пользователем** - Бот " \
               "сгенерирует и выдаст тебе список твоих чатов.\n**Выберу из списка контактов** - Бот сгенерирует и " \
               "выдаст тебе список твоих синхронизированых контактов в телеграм.\n**Перешлю его сообщение** - Нужно " \
               "переслать сообщение от пользователя боту. Важно! Некоторые пользователи поставили настройку " \
               "конфиденциальности и бот может не увидеть какого пользователя нужно пересылать"
        keyboard = keyboards.add
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def remove_step1(self, user_app):
        if not setting.user_setting[f'{self.chat_id}']["forward_setting"]:
            text = "Список пользователей на пересылку пуст!\nУдалять с пересылки некого!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на удаление с пересылки. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user_app, self.chat_id)
            text = "Выбери пересылку от какого пользователя удалить:"
            keyboard = await Keyboard().build(user_list, prefix="remove_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def remove_step2(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("remove_")
        remove_id = int(data)
        setting.del_forward(self.chat_id, remove_id)
        name = await GetInfo().get_user_name(user_app, remove_id)
        text = f"Пользователь **\"[{name}](tg://user?id={remove_id})\"** удалён из списка пересылки.\nКанал, куда " \
               f"пересылались сообщения остался не тронут, его ты должен удалить сам!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def freeze_step1(self, user_app):
        if not setting.user_setting[f"{self.chat_id}"]["forward_setting"]:
            text = "Список пользователей на пересылку пуст!\nЗамораживать пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на заморозку пересылки. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user_app, self.chat_id)
            text = "Выбери пересылку от какого пользователя заморозить:"
            keyboard = await Keyboard().build(user_list, prefix="freeze_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def freeze_step2(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("freeze_")
        freeze_id = int(data)
        setting.forward_contact_enable(self.chat_id, freeze_id, 0)
        name = await GetInfo().get_user_name(user_app, freeze_id)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={freeze_id})\"** ЗАМОРОЖЕНА!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def unfreeze_step1(self, user_app):
        if not setting.user_setting[f"{self.chat_id}"]:
            text = "Список пользователей на пересылку пуст!\nРазмораживать пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на разморозку пересылки. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user_app, self.chat_id)
            text = "Выбери пересылку от какого пользователя разморозить:"
            keyboard = await Keyboard().build(user_list, prefix="unfreeze_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def unfreeze_step2(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("unfreeze_")
        unfreeze_id = int(data)
        setting.forward_contact_enable(self.chat_id, unfreeze_id, 1)
        name = await GetInfo().get_user_name(user_app, unfreeze_id)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={unfreeze_id})\"** РАЗМОРОЖЕНА!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def change_destination_step1(self, user_app):
        if not setting.user_setting[f"{self.chat_id}"]["forward_setting"]:
            text = "Список пользователей на пересылку пуст!\nИзменять пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на изменение канала для пересылки. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user_app, self.chat_id)
            text = "Выбери какому пользователю изменить канал ля пересылки:"
            keyboard = await Keyboard().build(user_list, prefix="change_destination_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def change_destination_step2(self, user_app):
        text = "Подожди пожалуйста, получаю необходимую информацию..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        data = self.callback_data.data
        data = data.removeprefix("change_destination_")
        from_id = int(data)
        user_change = await GetInfo().get_user_name(user_app, from_id)
        text = f"Изменение канала для пересылки сообщений пользователя **\"[{user_change}](tg://user?id={from_id})\"" \
               f"\n\nВ какой канал пересылать сообщения?!"
        channel_list = await GetInfo().build_channel_list(user_app)
        setting.user_setting[f"{self.chat_id}"]["temp_uid"] = from_id
        keyboard = await Keyboard().build(channel_list, prefix="select_channel_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = ""
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def change_destination_step3(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("select_channel_")
        forward_to = int(data)
        user_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        setting.forward_edit_destination(self.chat_id, user_id, forward_to)
        name = await GetInfo().get_user_name(user_app, user_id)
        channel_name = await GetInfo().get_channel_name(user_app, forward_to)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={user_id})\"** перенаправлена в " \
               f"канал **\"{channel_name}\"**"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def forward_my_step1(self, user_app):
        if not setting.user_setting[f"{self.chat_id}"]["forward_setting"]:
            text = "У тебя нет никакой настроеной пересылки!\n\nЧто бы настроить пересылку собственных сообщений!"
            await self.client.answer_callback_query(self.callback_data.id,  text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на изменение пересылки своих сообщений. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user_app, self.chat_id)
            text = "Выбери в чате с каким пользователем ты хочешь изменить статус пересылки своих сообщений:"
            keyboard = await Keyboard().build(user_list, prefix="forward_my_step2_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def forward_my_step2(self, user_app):
        text = "Получаю информацию. Подожди немного..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        data = self.callback_data.data
        data = data.removeprefix("forward_my_step2_")
        data = int(data)
        user_info = await GetInfo().in_list(data, self.chat_id)
        user_name = await GetInfo().get_user_name(user_app, data)
        setting.user_setting[f"{self.chat_id}"]["temp_uid"] = data
        setting.user_setting[f"{self.chat_id}"]["temp_name"] = user_name
        keyboard = []
        if user_info[2]:
            text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={data})\"**" \
                   f" **ВКЛЮЧЕНА** ты можешь её **ОТКЛЮЧИТЬ**"
            keyboard = keyboards.forward_my_off
        elif not user_info[2]:
            text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={data})\"**" \
                   f" **ОТКЛЮЧЕНА** ты можешь её **ВКЛЮЧИТЬ**"
            keyboard = keyboards.forward_my_on
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def forward_my_on(self):
        user_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        user_name = setting.user_setting[f"{self.chat_id}"]["temp_name"]
        text = "Примененние настроек. Подожди немного..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        setting.forward_self(self.chat_id, user_id, 1)
        text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={user_id})\"**" \
               f" **ВКЛЮЧЕНА**! Теперь твои сообщения пересылаются тоже."
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def forward_my_off(self):
        user_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        user_name = setting.user_setting[f"{self.chat_id}"]["temp_name"]
        text = "Примененние настроек. Подожди немного..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        setting.forward_self(self.chat_id, user_id, 0)
        text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={user_id})\"**" \
               f" **ОТКЛЮЧЕНА**! Теперь твои сообщения не пересылаются."
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_send_contact_step1(self):
        text = "Теперь отправь контакт пользователя сюда. Для этого зайди в чат с пользователем, открой информацию о " \
               "нём, нажми три точки для открытия меню взаимодействия, затем пункт \"Поделиться контактом\""
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = "add_from_send_contact_step2"
        setting.user_setting[f"{self.chat_id}"]["temp_callbackdata"] = self.callback_data
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_send_contact_step2(self, user_app):
        callback_data = setting.user_setting[f"{self.chat_id}"]["temp_callbackdata"]
        if not self.message.contact:
            text = "Ты отправил не контакт! Попробуй ещё раз..."
            await self.client.send_message(self.chat_id, text=text)
            await self.message.delete()
        elif self.message.contact:
            from_id = self.message.contact.user_id
            in_list = await GetInfo().in_list(self.chat_id, from_id)
            if in_list:
                await self.message.delete()
                text = "Этот пользователь и так есть в списке пересылку!"
                await self.client.answer_callback_query(callback_data.id, text=text, show_alert=True)
            elif not in_list:
                text = "Подожди пожалуйста, получаю необходимую информацию..."
                await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
                user_to_add = await GetInfo().get_user_name(user_app, from_id)
                text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={from_id})\"** в пересылку.\n\n" \
                       f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений," \
                       f" или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- " \
                       f"Если ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                       f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в " \
                       f"один канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен" \
                       f" быть создателем канала!**"
                await self.client.delete_messages(self.chat_id, self.message_id)
                await self.message.delete()
                keyboard = keyboards.add_select_destination
                reply_markup = InlineKeyboardMarkup(keyboard)
                setting.temp_uid = from_id
                setting.temp_name = user_to_add
                await self.message.reply_text(text, reply_markup=reply_markup)

    async def add_from_exist_chat_step1(self, user_app):
        text = "Идёт подготовка списка чатов на добавление в пересылку. Подожди немного..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        user_list = await GetInfo().build_chat_list(user_app)
        text = "Выбери пересылку от какого пользователя разморозить:"
        keyboard = await Keyboard().build(user_list, prefix="exist_chat_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_exist_chat_step2(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("exist_chat_")
        user_id = int(data)
        in_list = await GetInfo().in_list(user_id, self.chat_id)
        if in_list:
            text = "Этот пользователь и так есть в списке пересылку!"
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        elif not in_list:
            text = "Подожди пожалуйста, получаю необходимую информацию..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_to_add = await GetInfo().get_user_name(user_app, user_id)
            text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={user_id})\"** в пересылку.\n\n" \
                   f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений, " \
                   f"или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- Если" \
                   f" ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать существующий" \
                   f"\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в один канал!\n- " \
                   f"Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен быть создателем " \
                   f"канала!**"
            keyboard = keyboards.add_select_destination
            reply_markup = InlineKeyboardMarkup(keyboard)
            setting.user_setting[f"{self.chat_id}"]["temp_uid"] = user_id
            setting.user_setting[f"{self.chat_id}"]["temp_name"] = user_to_add
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_sync_contact_step1(self, user_app):
        text = "Идёт подготовка списка синхронизированых контактов на добавление в пересылку. Подожди немного..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        user_list = await GetInfo().build_contact_list(user_app)
        text = "Выбери контакт какого пользователя хочешь добавить в пересылку:"
        keyboard = await Keyboard().build(user_list, prefix="sync_contact_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_sync_contact_step2(self, user_app):
        data = self.callback_data.data
        data = data.removeprefix("sync_contact_")
        user_id = int(data)
        in_list = await GetInfo().in_list(user_id, self.chat_id)
        if in_list:
            text = "Этот пользователь и так есть в списке пересылку!"
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        elif not in_list:
            text = "Подожди пожалуйста, получаю необходимую информацию..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            user_to_add = await GetInfo().get_user_name(user_app, user_id)
            text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={user_id})\"** в пересылку.\n\n" \
                   f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений, " \
                   f"или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- Если " \
                   f"ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                   f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в один " \
                   f"канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен быть " \
                   f"создателем канала!**"
            keyboard = keyboards.add_select_destination
            reply_markup = InlineKeyboardMarkup(keyboard)
            setting.user_setting[f"{self.chat_id}"]["temp_uid"] = user_id
            setting.user_setting[f"{self.chat_id}"]["temp_name"] = user_to_add
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_forwarded_message_step1(self):
        text = "Теперь отправь сюда одно из сообщений пользователя, сообщения которого нужно пересылать"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = "add_from_forwarded_message_step2"
        setting.user_setting[f"{self.chat_id}"]["temp_callbackdata"] = self.callback_data
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def add_from_forwarded_message_step2(self, user_app):
        callback_data = setting.user_setting[f"{self.chat_id}"]["temp_callbackdata"]  # todo fix
        if not self.message.forward_from:
            text = "Ты отправил не пересланное сообщение! Попробуй ещё раз... Или же ты отправил сообщение " \
                   "пользователя, у которого скрыта ссылка на аккаунт при пересылке сообщений!\nПопробуй другой" \
                   " способ добавления!"
            await self.client.send_message(self.chat_id, text=text)
            await self.message.delete()
        elif self.message.forward_from:
            from_id = self.message.forward_from.id
            in_list = await GetInfo().in_list(from_id, self.chat_id)
            if in_list:
                text = "Этот пользователь и так есть в списке пересылку!"
                await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
                await self.message.delete()
            elif not in_list:
                text = "Подожди пожалуйста, получаю необходимую информацию..."
                await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
                user_to_add = await GetInfo().get_user_name(user_app, from_id)
                text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={from_id})\"** в пересылку.\n\n" \
                       f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений," \
                       f" или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- " \
                       f"Если ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                       f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в " \
                       f"один канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен " \
                       f"быть создателем канала!**"
                await self.client.delete_messages(self.chat_id, self.message_id)
                await self.message.delete()
                keyboard = keyboards.add_select_destination
                reply_markup = InlineKeyboardMarkup(keyboard)
                setting.user_setting[f"{self.chat_id}"]["temp_uid"] = from_id
                setting.user_setting[f"{self.chat_id}"]["temp_name"] = user_to_add
                await self.message.reply_text(text, reply_markup=reply_markup)

    async def destination_create_new(self, user_app):
        from_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        name = setting.user_setting[f"{self.chat_id}"]["temp_name"]
        channel_name = f"{name} Сохранённые сообщения (id {from_id})"
        create_channel = await user_app.create_channel(channel_name, "Не удаляй, если используется пересылка, иначе бот упадёт при пересылке сообщений от этого юзера")
        forward_to = create_channel.id
        setting.add_to_forwarding(self.chat_id, from_id, forward_to)
        text = f"Пользователь **\"[{name}](tg://user?id={from_id})\"** добавлен в пересылку! Канал для пересылки " \
               f"**\"{channel_name}\"**"
        keyboard = keyboards.after_add
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = ""
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def destination_select_existing_step1(self, user_app):
        from_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        name = setting.user_setting[f"{self.chat_id}"]["temp_name"]
        text = "Подожди пока формируется список доступных каналов..."
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        channel_list = await GetInfo().build_channel_list(user_app)
        text = f"Выбери канал куда пересылать сообщения от **\"[{name}](tg://user?id={from_id})\"**"
        keyboard = await Keyboard().build(channel_list, prefix="select_existing_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["menu_point"] = ""
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def destination_select_existing_step2(self, user_app):
        from_id = setting.user_setting[f"{self.chat_id}"]["temp_uid"]
        name = setting.user_setting[f"{self.chat_id}"]["temp_name"]
        data = self.callback_data.data
        data = data.removeprefix("select_existing_")
        forward_to = int(data)
        setting.add_to_forwarding(self.chat_id, from_id, forward_to)
        channel_name = await GetInfo().get_channel_name(user_app, forward_to)
        text = f"Пользователь **\"[{name}](tg://user?id={from_id})\"** добавлен в пересылку! Канал для пересылки " \
               f"**\"{channel_name}\"**"
        keyboard = keyboards.after_add
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)
        setting.user_setting[f"{self.chat_id}"]["point"] = ""

    async def setting(self):
        text = "Выбери необходимый пункт настроек"
        keyboard = keyboards.setting
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.user_setting[f"{self.chat_id}"]["point"] = ""
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def about(self):
        await self.client.answer_callback_query(self.callback_data.id, text=about, show_alert=True)

    async def start(self):
        pause = setting.user_setting[f"{self.chat_id}"]["pause"]
        if not pause:
            text = "Бот и так уже работает!\n\nНажми \"Остановить бота\" если нужно будет остановить."
            await self.client.answer_callback_query(self.callback_data.id,  text=text, show_alert=True)
        elif pause:
            setting.pause(self.chat_id, 0)
            text = "Бот начал работу!\n\nНажми \"Остановить бота\" если нужно будет остановить."
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)

    async def stop(self):
        pause = setting.user_setting[f"{self.chat_id}"]["pause"]
        if not pause:
            setting.pause(self.chat_id, 1)
            text = "Бот остановлен!\n\nНажми \"Запустить бота\" если нужно будет запустить."
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        elif pause:
            text = "Бот и так уже остановлен!\n\nНажми \"Запустить бота\" если нужно будет запустить."
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)

    async def list(self, user_app):
        if not setting.user_setting[f"{self.chat_id}"]["forward_setting"]:
            text = "Список пользователей на пересылку пуст!\n\nТы можешь добавить их через \"Добавить в пересылку\""
            await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        else:
            text = "Список подготавливается к выдаче. Подожди немного..."
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
            text = await GetInfo().build_list(user_app, self.chat_id)
            keyboard = keyboards.bottom_button
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def help(self):  # TODO
        text = "Пока не доступно"
        await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)

    async def status(self):  # TODO
        if setting.user_setting[f"{self.chat_id}"]["pause"]:
            text = "Бот остановлен!"
        if not setting.user_setting[f"{self.chat_id}"]["pause"]:
            text = "Бот запущен!"
        await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)

    async def burn_all(self):
        text = "А теперь подумай хорошечно!"
        await self.client.answer_callback_query(self.callback_data.id, text=text, show_alert=True)
        text = "Пизда тебе досточка ёбаная\nИницыирую удаление всех аккаунтов и вайп каналов с пересылкой.\nТы точно" \
               " уверен(а), что хочешь всё вайпнуть К ХУЯМ?!\nЭТО ДЕЙСТВИЕ НЕ ОБРАТИМО!!!"
        keyboard = keyboards.burn_all
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def fbi_open_up(self, user_app):  # FIXME мб проблеми з вайпом через наплив повідомленнь
        text = "Начинаю вайпать к хуям все каналы и базу. ПОДОЖДИ БЛЭТ!"
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup="")
        for item in setting.user_setting[f"{self.chat_id}"]["forward_setting"]:
            await user_app.delete_channel(setting.user_setting[f"{self.chat_id}"]["forward_setting"][f"{item}"]["forward_to"])
            time.sleep(6)  # блядський ТГ потребує КД в 6сек
        setting.del_all_forwarding(self.chat_id)
        text = "Я ебу там уебало! Всё! Пизда рулю, снимай колёса! Всё вайпнуто! А теперь пошел нахуй!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.client.edit_message_text(chat_id=self.chat_id, message_id=self.message_id, text=text, reply_markup=reply_markup)

    async def upd_start(self):
        text = "Сейчас начнётся обновление бота, это может занять пару минут!\nВо время обновления пересылка " \
               "сообщений может быть недоступна!\nКогда обновление закончится - прийдёт уведомление."
        if self.message.from_user.id == admin_id:
            await self.message.reply_text("Начало отправки уведомлений...")
            for user in setting.user_setting:
                await self.client.send_message(int(user), text)
            await self.message.reply_text("Уведомление о начале обновления отправлено!")
        elif self.message.from_user.id != admin_id:
            await self.message.reply_text("Данная комманда доступна только администратору!")

    async def upd_end(self):
        text = f"Обновление завершено!\nТекущая версия бота {ver_app}\n{release_note}"
        if self.message.from_user.id == admin_id:
            await self.message.reply_text("Начало отправки уведомлений...")
            for user in setting.user_setting:
                await self.client.send_message(int(user), text)
            await self.message.reply_text("Уведомление об окончании обновления отправлено!")
        elif self.message.from_user.id != admin_id:
            await self.message.reply_text("Данная комманда доступна только администратору!")


class Keyboard:
    @staticmethod
    async def build(list_for_build, prefix):
        keyboard = []
        if prefix == "select_existing_":
            keyboard = copy.deepcopy(keyboards.select_existing)
        elif prefix == "remove_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        elif prefix == "freeze_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        elif prefix == "unfreeze_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        elif prefix == "select_channel_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        elif prefix == "exist_chat_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        elif prefix == "forward_my_step2_":
            keyboard = copy.deepcopy(keyboards.bottom_button)
        for item in list_for_build:
            i = [InlineKeyboardButton(item[0], callback_data=f"{prefix}{item[1]}")]
            keyboard.append(i)
        return keyboard


class GetInfo:  # todo fix new setting methods
    """Contain methods for building chats/channels/forwards info"""
    @staticmethod
    async def get_channel_name(client, channel_id):
        channel_info = await client.get_chat(channel_id)
        channel_name = channel_info.title
        return channel_name

    @staticmethod
    async def get_user_name(client, user_id):
        user = await client.get_users(user_id)
        if user.last_name:
            name = f"{user.first_name} {user.last_name}"
        else:
            name = user.first_name
        return name

    @staticmethod
    async def in_list(user_id, chat_id):
        """Return info for user in forward setting\n[forward_to, enable, forward_self]"""
        for item in setting.user_setting[f"{chat_id}"]["forward_setting"]:
            if int(item) == user_id:
                forward_to = setting.user_setting[f"{chat_id}"]["forward_setting"][f"{item}"]["forward_to"]
                enable = setting.user_setting[f"{chat_id}"]["forward_setting"][f"{item}"]["enable"]
                forward_self = setting.user_setting[f"{chat_id}"]["forward_setting"][f"{item}"]["forward_self"]
                f = [forward_to, enable, forward_self]
                return f

    @staticmethod
    async def is_register(user_id):
        for user in setting.user_setting:
            if user == str(user_id) and setting.user_setting[f"{user_id}"]['authorised']:
                return True

    async def build_user_forward_info(self, user_client, chat_id):
        user_list = []
        for user in setting.user_setting[f"{chat_id}"]["forward_setting"]:
            name = await self.get_user_name(user_client, int(user))
            user_list.append([name, int(user)])
        return user_list

    @staticmethod
    async def build_channel_list(user_client):
        channels = user_client.get_dialogs()
        channels_list = []
        async for item in channels:
            if item.chat.is_creator and str(item.chat.type) == "ChatType.CHANNEL":
                name = item.chat.title
                channel_id = item.chat.id
                channels_list.append([name, channel_id])
        return channels_list

    @staticmethod
    async def build_chat_list(user_client):
        chats = user_client.get_dialogs()
        chats_list = []
        async for item in chats:
            if str(item.chat.type) == "ChatType.PRIVATE":
                if item.chat.last_name:
                    name = f"{item.chat.first_name} {item.chat.last_name}"
                else:
                    name = item.chat.first_name
                chat_id = item.chat.id
                chats_list.append([name, chat_id])
        return chats_list

    @staticmethod
    async def build_contact_list(user_client):
        contacts = await user_client.get_contacts()
        users_list = []
        for user in contacts:
            if user.last_name:
                name = f"{user.first_name} {user.last_name}"
            else:
                name = user.first_name
            user_id = user.id
            users_list.append([name, user_id])
        return users_list

    async def build_list(self, user_client, chat_id):  # todo fix new setting methods
        """Need to build list of added user chat for forwarding. Return ready info string"""
        forward_setting = setting.user_setting[f"{chat_id}"]["forward_setting"]
        info = "Пользователи которые есть в списке на пересылку и информация о них:\n\n"
        list_id = 1
        for user in forward_setting:
            user_name = await self.get_user_name(user_client, int(user))
            prefs = forward_setting[f"{user}"]
            channel_info = await self.get_channel_name(user_client, prefs["forward_to"])
            freeze_info = ""
            self_forwarding = ""
            if prefs["forward_self"]:
                self_forwarding = "**ПЕРЕСЫЛАЮТСЯ**"
            if not prefs["forward_self"]:
                self_forwarding = "**НЕ ПЕРЕСЫЛАЮТСЯ**"
            if prefs["enable"]:
                freeze_info = "Пересылка **АКТИВНА**"
            if not prefs["enable"]:
                freeze_info = "Пересылка **ЗАМОРОЖЕНА**"
            info_string = f"__{list_id}__ - Сообщения от **\"[{user_name}](tg://user?id={user[0]})\"** пересылаются в" \
                          f" канал **\"{channel_info}**\". {freeze_info}. Мои сообщения {self_forwarding}.\n\n"
            info += info_string
            list_id += 1
        return info

    @staticmethod
    async def get_user_app(user_id, users):
        name = f"u{user_id}"
        for app in users:
            if app.name == name:
                return app


class UserAuth:

    @staticmethod
    async def create_app(user_id, phone_number):
        app = Client(f"u{user_id}", api_id=api_id, api_hash=api_hash, app_version=name_app+ver_app,
                     device_model=device_model, system_version=system_version)
        await app.connect()
        sc = await app.send_code(phone_number=phone_number)
        apps.append([app, sc, phone_number])

    @staticmethod
    async def auth_code(user_id, phone_code):
        for app in apps:
            if app[0].name == f"u{user_id}":
                pch = app[1].phone_code_hash
                await app[0].sign_in(phone_number=app[2], phone_code_hash=pch, phone_code=phone_code)
                await app[0].disconnect()
