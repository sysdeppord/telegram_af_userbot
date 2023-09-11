from cp_bot import keyboards
from pyrogram.types import InlineKeyboardMarkup
from proxy_class import setting
from config.tg_config import god_code


class AdminPanel:

    async def cmd_processor(self, client, callback):
        if callback.data == "a_panel":
            await self.admin_menu(client, callback)
        elif callback.data == "a_stats":
            await self.a_stats(client, callback)
        elif callback.data == "a_users":
            await self.a_users(client, callback)
        elif callback.data == "a_ban":
            await self.a_ban(client, callback)
        elif callback.data == "a_unban":
            await self.a_unban(client, callback)
        elif callback.data == "a_make_admin":
            await self.a_make_admin(client, callback)
        elif callback.data == "a_ban_admin":
            await self.a_ban_admin(client, callback)
        elif callback.data == "a_view_requests":
            await self.a_view_requests(client, callback)
        elif callback.data == "a_create_invite":
            await self.a_create_invite(client, callback)

    @staticmethod
    async def admin_menu(client, callback):
        text = "Добро пожаловать в админ панель! Выбери что нужно сделать:"
        keyboard = keyboards.admin_menu
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def god_mode(client, message):
        god_command = message.text.split()
        god_message = god_command[1]
        if god_code == god_message:
            setting.set_admin(message.from_user.id, 1)
            await message.reply_text("CONGRATULATION you have admin rights!!!\n/start")

    @staticmethod
    async def a_stats(client, callback):
        text = "Заглушка меню статистики"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_users(client, callback):
        text = await APanelFunctional().build_user_list(client)
        print(text)
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_ban(client, callback):
        text = "Заглушка меню бана пользователей"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_unban(client, callback):
        text = "Заглушка меню разбана пользователей"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_make_admin(client, callback):
        text = "Заглушка меню добавления администраторов"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_ban_admin(client, callback):
        text = "Заглушка меню снятия администраторов"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_view_requests(client, callback):
        text = "Заглушка меню просмотра запросов на регистрацию"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)

    @staticmethod
    async def a_create_invite(client, callback):
        text = "Заглушка меню просмотра запросов на регистрацию"
        keyboard = keyboards.a_bottom_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await client.edit_message_text(text=text, chat_id=callback.message.chat.id, message_id=callback.message.id,
                                       reply_markup=reply_markup)


class APanelFunctional:

    async def build_user_list(self, client):
        text = ""
        users = await self.get_user(client, setting.user_setting)
        for user in users:
            text += await self.build_user_string_info(user)
        return text

    @staticmethod
    async def build_user_string_info(user):
        user_setting = setting.user_setting[f"{user.id}"]
        if user.last_name:
            name = f"{user.first_name} {user.last_name}"
        else:
            name = user.first_name
        count_forward = len(user_setting["forward_setting"])
        if user_setting["is_blocked"]:
            blocked = "ДА"
        else:
            blocked = "НЕТ"
        if user_setting["pause"]:
            pause = "остановлен"
        else:
            pause = "запущен"
        if user_setting["is_admin"]:
            admin = "ДА"
        else:
            admin = "НЕТ"
        info = (f"- {name} (id{user.id}) == Бот {pause}, пользователь заблокирован - {blocked}, пересылок настроено -"
                f" {count_forward}, администаратор - {admin}\n\n")
        return info

    @staticmethod
    async def get_user(client, users_ids):
        users = await client.get_users(users_ids)
        return users


