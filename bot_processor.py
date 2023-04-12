import copy
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keyboards

admin_id = 0  # CHANGE_ME for dual control
about = "Forward bot by: @SYSdeppord\nv 0.0.4.0 nightly\nPowered by: SYSdeppord govno cloud"
release_note = "Что нового?\n" \
               "- Переход с управление командами на управление кнопками! Теперь достаточно нажать /start дабы " \
               "получить лёгкий доступ к меню бота!\n" \
               "- Добавлена возможность добавление нового пользователя в пересылку сразу после следующего!\n" \
               "- Переписан движок бота для возможности лёгкого добавления новых функций!\n" \
               "- Возможно небольшие улучшения в скорости работы.\n" \
               "- Пофиксил старые баги и добавил новые!\n\n\n" \
               "Предложения/пожелания/багрепорты приветствуются -> @SYSdeppord"


class Sorter:
    @staticmethod
    async def callback_filter(client, user, callback_data, setting):
        data = callback_data.data
        processor = Processor()
        if data == "setting":
            await processor.setting(client, callback_data, setting)
        elif data == "start":
            await processor.start(client, callback_data, setting)
        elif data == "stop":
            await processor.stop(client, callback_data, setting)
        elif data == "add":
            await processor.add(client, callback_data)
        elif data == "remove_step1":
            await processor.remove_step1(client, user, callback_data, setting)
        elif data == "freeze_step1":
            await processor.freeze_step1(client, user, callback_data, setting)
        elif data == "unfreeze_step1":
            await processor.unfreeze_step1(client, user, callback_data, setting)
        elif data == "forward_my_step1":
            await processor.forward_my_step1(client, user, callback_data, setting)
        elif data == "change_destination_step1":
            await processor.change_destination_step1(client, user, callback_data, setting)
        elif data == "main_menu":
            await processor.main_menu(client, callback_data, setting)
        elif data == "about":
            await processor.about(client, callback_data)
        elif data == "status":
            await processor.status(client, callback_data)
        elif data == "list":
            await processor.list(client, user, callback_data, setting)
        elif data == "help":
            await processor.help(client, callback_data)
        elif data.startswith("select_existing_"):
            await processor.destination_select_existing_step2(client, user, callback_data, setting)
        elif data.startswith("remove_"):
            await processor.remove_step2(client, user, callback_data, setting)
        elif data.startswith("freeze_"):
            await processor.freeze_step2(client, user, callback_data, setting)
        elif data.startswith("unfreeze_"):
            await processor.unfreeze_step2(client, user, callback_data, setting)
        elif data.startswith("change_destination_"):
            await processor.change_destination_step2(client, user, callback_data, setting)
        elif data.startswith("exist_chat_"):
            await processor.add_from_exist_chat_step2(client, user, callback_data, setting)
        elif data.startswith("sync_contact_"):
            await processor.add_from_sync_contact_step2(client, user, callback_data, setting)
        elif data.startswith("forward_my_step2_"):
            await processor.forward_my_step2(client, user, callback_data, setting)
        elif data == "add_from_send_contact_step1":
            await processor.add_from_send_contact_step1(client, callback_data, setting)
        elif data == "add_from_exist_chat_step1":
            await processor.add_from_exist_chat_step1(client, user, callback_data)
        elif data == "add_from_sync_contact_step1":
            await processor.add_from_sync_contact_step1(client, user, callback_data)
        elif data == "add_from_forwarded_message_step1":
            await processor.add_from_forwarded_message_step1(client, callback_data, setting)
        elif data == "destination_create_new":
            await processor.destination_create_new(client, user, callback_data, setting)
        elif data == "destination_select_existing_step1":
            await processor.destination_select_existing_step1(client, user, callback_data, setting)
        elif data == "burn_all":
            await processor.burn_all(client, callback_data)
        elif data == "fbi_open_up":
            await processor.fbi_open_up(client, user, callback_data, setting)
        elif data == "forward_my_off":
            await processor.forward_my_off(client, callback_data, setting)
        elif data == "forward_my_on":
            await processor.forward_my_on(client, callback_data, setting)

    @staticmethod
    async def message_filter(bot, user, message, setting):
        processor = Processor()
        if message.from_user.id == setting.my_id or message.from_user.id == admin_id:
            if message.text == "/start":
                await processor.start_message(message, setting)
            if setting.point == "add_from_send_contact_step2":
                await processor.add_from_send_contact_step2(bot, user, message, setting)
            if setting.point == "add_from_forwarded_message_step2":
                await processor.add_from_forwarded_message_step2(bot, user, message, setting)
            if message.text == "/upd_start":
                await processor.upd_start(bot, message, setting)
            if message.text == "/upd_end":
                await processor.upd_end(bot, message, setting)
        else:
            await message.reply_text("Ты пока не можешь пользоваться данным ботом!\nНапиши @SYSdeppord чтобы попасть"
                                     " в следующий этап тестирования")


class Processor:

    @staticmethod
    async def start_message(message, setting):  # TODO
        text = "Привет!\nЭто бот для автоматической пересылки!\nДля навигации по меню используй кнопки ниже!"
        keyboard = keyboards.start_message
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def main_menu(client, callback_data, setting):  # TODO
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Привет!\nЭто бот для автоматической пересылки!\nДля навигации по меню используй кнопки ниже!"
        keyboard = keyboards.start_message
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add(client, callback_data):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Выбери как добавить пользователя:\n\n**Отправлю контакт пользователя** - Нужно зайти в чат с " \
               "пользователем, нажать **поделиться** и отправить контакт боту.\n**Выберу чат с пользователем** - Бот " \
               "сгенерирует и выдаст тебе список твоих чатов.\n**Выберу из списка контактов** - Бот сгенерирует и " \
               "выдаст тебе список твоих синхронизированых контактов в телеграм.\n**Перешлю его сообщение** - Нужно " \
               "переслать сообщение от пользователя боту. Важно! Некоторые пользователи поставили настройку " \
               "конфиденциальности и бот может не увидеть какого пользователя нужно пересылать"
        keyboard = keyboards.add
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def remove_step1(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "Список пользователей на пересылку пуст!\nУдалять с пересылки некого!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на удаление с пересылки. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user, setting.forward_setting)
            text = "Выбери пересылку от какого пользователя удалить:"
            keyboard = await Keyboard().build(user_list, prefix="remove_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def remove_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("remove_")
        remove_id = int(data)
        setting.del_forward(remove_id)
        name = await GetInfo().get_user_name(user, remove_id)
        text = f"Пользователь **\"[{name}](tg://user?id={remove_id})\"** удалён из списка пересылки.\nКанал, куда " \
               f"пересылались сообщения остался не тронут, его ты должен удалить сам!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def freeze_step1(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "Список пользователей на пересылку пуст!\nЗамораживать пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на заморозку пересылки. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user, setting.forward_setting)
            text = "Выбери пересылку от какого пользователя заморозить:"
            keyboard = await Keyboard().build(user_list, prefix="freeze_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def freeze_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("freeze_")
        freeze_id = int(data)
        setting.forward_contact_enable(freeze_id, 0)
        name = await GetInfo().get_user_name(user, freeze_id)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={freeze_id})\"** ЗАМОРОЖЕНА!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def unfreeze_step1(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "Список пользователей на пересылку пуст!\nРазмораживать пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на разморозку пересылки. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user, setting.forward_setting)
            text = "Выбери пересылку от какого пользователя разморозить:"
            keyboard = await Keyboard().build(user_list, prefix="unfreeze_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def unfreeze_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("unfreeze_")
        unfreeze_id = int(data)
        setting.forward_contact_enable(unfreeze_id, 1)
        name = await GetInfo().get_user_name(user, unfreeze_id)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={unfreeze_id})\"** РАЗМОРОЖЕНА!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def change_destination_step1(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "Список пользователей на пересылку пуст!\nИзменять пересылку некому!\n\nТы можешь добавить их" \
                   " через меню \"Добавить в пересылку\""
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на изменение канала для пересылки. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user, setting.forward_setting)
            text = "Выбери какому пользователю изменить канал ля пересылки:"
            keyboard = await Keyboard().build(user_list, prefix="change_destination_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def change_destination_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Подожди пожалуйста, получаю необходимую информацию..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        data = callback_data.data
        data = data.removeprefix("change_destination_")
        from_id = int(data)
        user_change = await GetInfo().get_user_name(user, from_id)
        text = f"Изменение канала для пересылки сообщений пользователя **\"[{user_change}](tg://user?id={from_id})\"" \
               f"\n\nВ какой канал пересылать сообщения?!"
        channel_list = await GetInfo().build_channel_list(user)
        setting.temp_uid = from_id
        keyboard = await Keyboard().build(channel_list, prefix="select_channel_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def change_destination_step3(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("select_channel_")
        forward_to = int(data)
        user_id = setting.temp_uid
        setting.forward_edit_destination(user_id, forward_to)
        name = await GetInfo().get_user_name(user, user_id)
        channel_name = await GetInfo().get_channel_name(user, forward_to)
        text = f"Пересылка сообщений от пользователя **\"[{name}](tg://user?id={user_id})\"** перенаправлена в " \
               f"канал **\"{channel_name}\"**"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def forward_my_step1(client, user, callback_data, setting):  # TODO
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "У тебя нет никакой настроеной пересылки!\n\nЧто бы настроить пересылку собственных сообщений!"
            await client.answer_callback_query(callback_data.id,  text=text, show_alert=True)
        else:
            text = "Идёт подготовка списка на изменение пересылки своих сообщений. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_list = await GetInfo().build_user_forward_info(user, setting.forward_setting)
            text = "Выбери в чате с каким пользователем ты хочешь измеить статус пересылки своих сообщений:"
            keyboard = await Keyboard().build(user_list, prefix="forward_my_step2_")
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def forward_my_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Получаю информацию. Подожди немного..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        data = callback_data.data
        data = data.removeprefix("forward_my_step2_")
        data = int(data)
        user_info = await GetInfo().in_list(data, setting)
        user_name = await GetInfo().get_user_name(user, data)
        setting.temp_uid = data
        setting.temp_name = user_name
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
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def forward_my_on(client, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        user_id = setting.temp_uid
        user_name = setting.temp_name
        text = "Примененние настроек. Подожди немного..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        setting.forward_self(user_id, 1)
        text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={user_id})\"**" \
               f" **ВКЛЮЧЕНА**! Теперь твои сообщения пересылаются тоже."
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def forward_my_off(client, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        user_id = setting.temp_uid
        user_name = setting.temp_name
        text = "Примененние настроек. Подожди немного..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        setting.forward_self(user_id, 0)
        text = f"Пересылка своих сообщений в чате с пользователем **\"[{user_name}](tg://user?id={user_id})\"**" \
               f" **ОТКЛЮЧЕНА**! Теперь твои сообщения не пересылаются."
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def code(client, data, setting):  # TODO
        # Future
        pass

    @staticmethod
    async def add_from_send_contact_step1(client, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Теперь отправь контакт пользователя сюда. Для этого зайди в чат с пользователем, открой информацию о " \
               "нём, нажми три точки для открытия меню взаимодействия, затем пункт \"Поделиться контактом\""
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = "add_from_send_contact_step2"
        setting.temp_callbackdata = callback_data
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_send_contact_step2(client, user, message, setting):
        callback_data = setting.temp_callbackdata
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not message.contact:
            text = "Ты отправил не контакт! Попробуй ещё раз..."
            await client.send_message(chat_id, text=text)
            await message.delete()
        elif message.contact:
            from_id = message.contact.user_id
            in_list = await GetInfo().in_list(from_id, setting)
            if in_list:
                await message.delete()
                text = "Этот пользователь и так есть в списке пересылку!"
                await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
            elif not in_list:
                text = "Подожди пожалуйста, получаю необходимую информацию..."
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
                user_to_add = await GetInfo().get_user_name(user, from_id)
                text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={from_id})\"** в пересылку.\n\n" \
                       f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений," \
                       f" или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- " \
                       f"Если ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                       f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в " \
                       f"один канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен" \
                       f" быть создателем канала!**"
                await client.delete_messages(chat_id, message_id)
                await message.delete()
                keyboard = keyboards.add_select_destination
                reply_markup = InlineKeyboardMarkup(keyboard)
                setting.temp_uid = from_id
                setting.temp_name = user_to_add
                await message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_exist_chat_step1(client, user, callback_data):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Идёт подготовка списка чатов на добавление в пересылку. Подожди немного..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        user_list = await GetInfo().build_chat_list(user)
        text = "Выбери пересылку от какого пользователя разморозить:"
        keyboard = await Keyboard().build(user_list, prefix="exist_chat_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_exist_chat_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("exist_chat_")
        user_id = int(data)
        in_list = await GetInfo().in_list(user_id, setting)
        if in_list:
            text = "Этот пользователь и так есть в списке пересылку!"
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        elif not in_list:
            text = "Подожди пожалуйста, получаю необходимую информацию..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_to_add = await GetInfo().get_user_name(user, user_id)
            text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={user_id})\"** в пересылку.\n\n" \
                   f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений, " \
                   f"или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- Если" \
                   f" ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать существующий" \
                   f"\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в один канал!\n- " \
                   f"Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен быть создателем " \
                   f"канала!**"
            keyboard = keyboards.add_select_destination
            reply_markup = InlineKeyboardMarkup(keyboard)
            setting.temp_uid = user_id
            setting.temp_name = user_to_add
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_sync_contact_step1(client, user, callback_data):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Идёт подготовка списка синхронизированых контактов на добавление в пересылку. Подожди немного..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        user_list = await GetInfo().build_contact_list(user)
        text = "Выбери пересылку от какого пользователя разморозить:"
        keyboard = await Keyboard().build(user_list, prefix="sync_contact_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_sync_contact_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        data = callback_data.data
        data = data.removeprefix("sync_contact_")
        user_id = int(data)
        in_list = await GetInfo().in_list(user_id, setting)
        if in_list:
            text = "Этот пользователь и так есть в списке пересылку!"
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        elif not in_list:
            text = "Подожди пожалуйста, получаю необходимую информацию..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            user_to_add = await GetInfo().get_user_name(user, user_id)
            text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={user_id})\"** в пересылку.\n\n" \
                   f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений, " \
                   f"или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- Если " \
                   f"ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                   f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в один " \
                   f"канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен быть " \
                   f"создателем канала!**"
            keyboard = keyboards.add_select_destination
            reply_markup = InlineKeyboardMarkup(keyboard)
            setting.temp_uid = user_id
            setting.temp_name = user_to_add
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_forwarded_message_step1(client, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Теперь отправь сюда одно из сообщений пользователя, сообщения которого нужно пересылать"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = "add_from_forwarded_message_step2"
        setting.temp_callbackdata = callback_data
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def add_from_forwarded_message_step2(client, user, message, setting):
        callback_data = setting.temp_callbackdata
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not message.forward_from:
            text = "Ты отправил не пересланное сообщение! Попробуй ещё раз... Или же ты отправил сообщение " \
                   "пользователя, у которого скрыта ссылка на аккаунт при пересылке сообщений!\nПопробуй другой" \
                   " способ добавления!"
            await client.send_message(chat_id, text=text)
            await message.delete()
        elif message.forward_from:
            from_id = message.forward_from.id
            in_list = await GetInfo().in_list(from_id, setting)
            if in_list:
                text = "Этот пользователь и так есть в списке пересылку!"
                await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
                await message.delete()
            elif not in_list:
                text = "Подожди пожалуйста, получаю необходимую информацию..."
                await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
                user_to_add = await GetInfo().get_user_name(user, from_id)
                text = f"Добавление пользователя **\"[{user_to_add}](tg://user?id={from_id})\"** в пересылку.\n\n" \
                       f"Теперь выбери нужное действие.\n- Если у тебя нету созданого канала для пересылки сообщений," \
                       f" или ты хочешь чтобы был создан новый - выбери пункт **\"🆕 Создать автоматически\"**\n- " \
                       f"Если ты уже имеешь нужный канал для пересылки сообщений - выбери пункт **\"➕ Выбрать " \
                       f"существующий\"**\n\n**ВНИМАНИЕ!\n- Не советую смешивать пересылку разных пользователей в " \
                       f"один канал!\n- Канал для пересылки сообщений **НЕ ДОЛЖЕН** быть общедоступным!\n- Ты должен " \
                       f"быть создателем канала!**"
                await client.delete_messages(chat_id, message_id)
                await message.delete()
                keyboard = keyboards.add_select_destination
                reply_markup = InlineKeyboardMarkup(keyboard)
                setting.temp_uid = from_id
                setting.temp_name = user_to_add
                await message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def destination_create_new(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        from_id = setting.temp_uid
        name = setting.temp_name
        channel_name = f"{name} Сохранённые сообщения (id {from_id})"
        create_channel = await user.create_channel(channel_name, "Не удаляй, если используется пересылка, иначе бот "
                                                                 "упадёт при пересылке сообщений от этого юзера")
        forward_to = create_channel.id
        setting.add_to_forwarding(from_id, forward_to)
        text = f"Пользователь **\"[{name}](tg://user?id={from_id})\"** добавлен в пересылку! Канал для пересылки " \
               f"**\"{channel_name}\"**"
        keyboard = keyboards.after_add
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def destination_select_existing_step1(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        from_id = setting.temp_uid
        name = setting.temp_name
        text = "Подожди пока формируется список доступных каналов..."
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        channel_list = await GetInfo().build_channel_list(user)
        text = f"Выбери канал куда пересылать сообщения от **\"[{name}](tg://user?id={from_id})\"**"
        keyboard = await Keyboard().build(channel_list, prefix="select_existing_")
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def destination_select_existing_step2(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        from_id = setting.temp_uid
        name = setting.temp_name
        data = callback_data.data
        data = data.removeprefix("select_existing_")
        forward_to = int(data)
        setting.add_to_forwarding(from_id, forward_to)
        channel_name = await GetInfo().get_channel_name(user, forward_to)
        text = f"Пользователь **\"[{name}](tg://user?id={from_id})\"** добавлен в пересылку! Канал для пересылки " \
               f"**\"{channel_name}\"**"
        keyboard = keyboards.after_add
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)
        setting.point = ""

    @staticmethod
    async def setting(client, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Выбери необходимый пункт настроек"
        keyboard = keyboards.setting
        reply_markup = InlineKeyboardMarkup(keyboard)
        setting.point = ""
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def about(client, callback_data):
        await client.answer_callback_query(callback_data.id, text=about, show_alert=True)

    @staticmethod
    async def start(client, callback_data, setting):
        pause = setting.is_pause
        if not pause:
            text = "Бот и так уже работает!\n\nНажми \"Остановить бота\" если нужно будет остановить."
            await client.answer_callback_query(callback_data.id,  text=text, show_alert=True)
        elif pause:
            setting.pause(0)
            text = "Бот начал работу!\n\nНажми \"Остановить бота\" если нужно будет остановить."
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)

    @staticmethod
    async def stop(client, callback_data, setting):
        pause = setting.is_pause
        if not pause:
            setting.pause(1)
            text = "Бот остановлен!\n\nНажми \"Запустить бота\" если нужно будет запустить."
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        elif pause:
            text = "Бот и так уже остановлен!\n\nНажми \"Запустить бота\" если нужно будет запустить."
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)

    @staticmethod
    async def list(client, user, callback_data, setting):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        if not setting.forward_setting:
            text = "Список пользователей на пересылку пуст!\n\nТы можешь добавить их через \"Добавить в пересылку\""
            await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        else:
            text = "Список подготавливается к выдаче. Подожди немного..."
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
            text = await GetInfo().build_list(user, setting)
            keyboard = keyboards.bottom_button
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def help(client, callback_data):  # TODO
        text = "Пока не доступно"
        await client.answer_callback_query(callback_data.id, text=text, show_alert=True)

    @staticmethod
    async def status(client, callback_data):  # TODO
        text = "Пока не доступно"
        await client.answer_callback_query(callback_data.id, text=text, show_alert=True)

    @staticmethod
    async def burn_all(client, callback_data):
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "А теперь подумай хорошечно!"
        await client.answer_callback_query(callback_data.id, text=text, show_alert=True)
        text = "Пизда тебе досточка ёбаная\nИницыирую удаление всех аккаунтов и вайп каналов с пересылкой.\nТы точно" \
               " уверен(а), что хочешь всё вайпнуть К ХУЯМ?!\nЭТО ДЕЙСТВИЕ НЕ ОБРАТИМО!!!"
        keyboard = keyboards.burn_all
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def fbi_open_up(client, user, callback_data, setting):  # todo мб проблеми з вайпом через наплив повідомленнь
        chat_id = callback_data.from_user.id
        message_id = callback_data.message.id
        text = "Начинаю вайпать к хуям все каналы и базу. ПОДОЖДИ БЛЭТ!"
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup="")
        for item in setting.forward_setting:
            await user.delete_channel(item[1])
            time.sleep(6)  # It is necessary not to flood (Telegram needs 6 seconds)
        setting.del_all_forwarding()
        text = "Я ебу там уебало! Всё! Пизда рулю, снимай колёса! Всё вайпнуто! А теперь пошел нахуй!"
        keyboard = keyboards.bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)

    @staticmethod
    async def upd_start(client, message, setting):
        text = "Сейчас начнётся обновление бота, это может занять пару минут!\nВо время обновления пересылка " \
               "сообщений может быть недоступна!\nКогда обновление закончится - прийдёт уведомление."
        if message.from_user.id == admin_id:
            await client.send_message(setting.my_id, text)
            await message.reply_text("Уведомление о начале обновления отправлено!")
        elif message.from_user.id == setting.my_id:
            await message.reply_text("Данная комманда доступна только администратору!")

    @staticmethod
    async def upd_end(client, message, setting):
        text = f"Обновление завершено!\nТекущая версия бота {about}\n{release_note}"
        if message.from_user.id == admin_id:
            await client.send_message(setting.my_id, text)
            await message.reply_text("Уведомление об окончании обновления отправлено!")
        elif message.from_user.id == setting.my_id:
            await message.reply_text("Данная комманда доступна только администратору!")


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


class GetInfo:
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
    async def in_list(user_id, setting):
        """Return info for user in forward setting\n0 - forward_to, 1 - enable, 2 - forward_self"""
        for item in setting.forward_setting:
            if item[0] == user_id:
                f = [item[1], item[2], item[3]]
                return f

    async def build_user_forward_info(self, user_client, setting):
        print(setting)
        user_list = []
        for user in setting:
            name = await self.get_user_name(user_client, user[0])
            user_id = user[0]
            user_list.append([name, user_id])
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

    async def build_list(self, user_client, setting):
        """Need to build list of added user chat for forwarding. Return ready info string"""
        forward_setting = setting.forward_setting
        info = "Пользователи которые есть в списке на пересылку и информация о них:\n\n"
        list_id = 1
        for user in forward_setting:
            # 0 - user, 1 - forward_to, 2 - enable, 3 - forward_self
            user_name = await self.get_user_name(user_client, user[0])
            channel_info = await self.get_channel_name(user_client, user[1])
            freeze_info = ""
            self_forwarding = ""
            if user[3]:
                self_forwarding = "**ПЕРЕСЫЛАЮТСЯ**"
            if not user[3]:
                self_forwarding = "**НЕ ПЕРЕСЫЛАЮТСЯ**"
            if user[2]:
                freeze_info = "Пересылка **АКТИВНА**"
            if not user[2]:
                freeze_info = "Пересылка **ЗАМОРОЖЕНА**"
            info_string = f"__{list_id}__ - Сообщения от **\"[{user_name}](tg://user?id={user[0]})\"** пересылаются в" \
                          f" канал **\"{channel_info}**\". {freeze_info}. Мои сообщения {self_forwarding}.\n\n"
            info += info_string
            list_id += 1
        return info
