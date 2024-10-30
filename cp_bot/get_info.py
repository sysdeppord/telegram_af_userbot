from pyrogram import errors
from proxy_class import setting


class GetInfo:
    """Contain methods for building chats/channels/forwards info"""
    @staticmethod
    async def get_channel_name(client, channel_id):
        try:
            channel_info = await client.get_chat(channel_id)
            channel_name = channel_info.title
            return channel_name
        except errors.ChannelPrivate:
            return "КАНАЛ УДАЛЁН ИЛИ НЕДОСТУПЕН!!!"

    async def get_user_name(self, client, user_id):
        name = None
        try:
            if user_id > 0:
                user = await client.get_users(user_id)
                if user.last_name:
                    name = f"{user.first_name} {user.last_name}"
                else:
                    name = user.first_name
            elif user_id < 0:
                name = await self.get_channel_name(client, user_id)
        except errors.PeerIdInvalid as e:
            name = f"Пользователь не найден! Попробуй передобавить этого пользователя заново.\nTelegram error:\n{e}"
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
            if user.startswith("-"):
                name = await self.get_channel_name(user_client, int(user))
            else:
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
    async def build_chat_list(user_client, flag=None):
        chats = user_client.get_dialogs()
        chats_list = []
        if not flag:
            async for item in chats:
                if str(item.chat.type) == "ChatType.PRIVATE":
                    if item.chat.last_name:
                        name = f"{item.chat.first_name} {item.chat.last_name}"
                    else:
                        name = item.chat.first_name
                    chat_id = item.chat.id
                    chats_list.append([name, chat_id])
        if flag == "channel":
            async for item in chats:
                if str(item.chat.type) == "ChatType.CHANNEL":
                    name = item.chat.title
                    channel_id = item.chat.id
                    chats_list.append([name, channel_id])
        elif flag == "group":
            async for item in chats:
                if str(item.chat.type) == "ChatType.GROUP" or str(item.chat.type) == "ChatType.SUPERGROUP":
                    name = item.chat.title
                    group_id = item.chat.id
                    chats_list.append([name, group_id])
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

    async def build_list(self, user_client, chat_id):
        """Need to build list of added user chat for forwarding. Return ready info string"""
        forward_setting = setting.user_setting[f"{chat_id}"]["forward_setting"]
        info = "Пользователи которые есть в списке на пересылку и информация о них:\n\n"
        list_id = 1
        for user in forward_setting:
            if user.startswith("-"):
                user_name = await self.get_channel_name(user_client, int(user))
            else:
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
            if users[app].name == name:
                return users[app]
