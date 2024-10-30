from datetime import datetime, timedelta
import copy
from pyrogram import errors
from pyrogram.types import InputMediaDocument
from proxy_class import setting
import time

cooldown = 10  # cd for scheduled messages


class UserMessages:
    """All forward logic"""

    async def forward_logic(self, client, message, bot_client):
        user = client.name.replace("u", "")
        user_setting = setting.user_setting[f"{user}"]
        user_setting = copy.deepcopy(user_setting)
        is_pause = user_setting["pause"]
        if message.service:
            if str(message.service) == "MessageServiceType.MIGRATE_TO_CHAT_ID":
                await self.migrate_chat_id(client, message)
        elif not is_pause:
            if f"{message.chat.id}" in setting.user_setting[f"{user}"]["forward_setting"]:  # in user_setting["forward_setting"]:
                # forward_from = setting.user_setting[f"{user}"]["forward_setting"][f"{message.chat.id}"]
                forward_to = setting.user_setting[f"{user}"]["forward_setting"][f"{message.chat.id}"]["forward_to"]
                enable_forwarding = setting.user_setting[f"{user}"]["forward_setting"][f"{message.chat.id}"]["enable"]
                forward_self = setting.user_setting[f"{user}"]["forward_setting"][f"{message.chat.id}"]["forward_self"]
                user_id = message.from_user.id
                my_id = int(user)
                protected = None
                try:
                    if message.chat.has_protected_content:
                        protected = True
                    elif not message.chat.has_protected_content:
                        protected = False

                    if enable_forwarding:
                        if user_id == my_id:
                            if forward_self:
                                await self.forward_processor(message, forward_to, client, protected, my_id)
                        else:
                            await self.forward_processor(message, forward_to, client, protected, my_id)
                except errors.ChannelPrivate:
                    await self.channel_error_message(message, bot_client, my_id)
                    setting.forward_contact_enable(my_id, message.chat.id, 0)

    @staticmethod
    async def migrate_chat_id(client, message):
        print("migrate")
        print(message)
        old_id = message.chat.id
        new_id = message.migrate_to_chat_id
        client_name = client.name
        user_id = client_name.replace("u", "")
        for chat in setting.user_setting[f"{user_id}"]["forward_setting"]:
            print(chat)
            if str(chat) == str(old_id):
                print("catched")
        print(f"from {old_id} to {new_id}")
        setting.migrate_chat_id(user_id, old_id, new_id)

    @staticmethod
    async def channel_error_message(message, bot_client, user_id):
        if not message.from_user:
            name = message.chat.title
        elif message.from_user.last_name:
            name = f"{message.from_user.first_name} {message.from_user.last_name}"
        else:
            name = message.from_user.first_name
        text = f"Канал, в который пересылаются сообщения от **\"{name}\"** недоступен!!! Пересылка заморожена! Измени" \
               f" канал назначения пересылки в настройках!"
        await bot_client.send_message(chat_id=user_id, text=text)

    async def forward_processor(self, message, forward_to, client, protected, my_id):
        dt = datetime.now()
        date = dt + timedelta(seconds=cooldown)
        if protected:
            try:
                await self.forward_protected_content_from_cg(message, forward_to, client, my_id)
            except ValueError:
                if not message.from_user:
                    name = message.chat.title
                elif message.from_user.last_name:
                    name = f"{message.from_user.first_name} {message.from_user.last_name}"
                else:
                    name = message.from_user.first_name
                if message.media:
                    type_media = message.media
                else:
                    type_media = "UNKNOWN MESSAGE"
                text = f"Сообщене с защищённого канала/группы от пользователя \"{name}\", дата и " \
                       f"время сообщения \"{str(message.date)}\"\n- Данный тип сообщения **\"{type_media}\"** не " \
                       f"возможно переслать с защищенного канала/группы."
                dt = datetime.now()
                date = dt + timedelta(seconds=cooldown)
                await client.send_message(chat_id=forward_to, text=text, disable_notification=True, schedule_date=date)
        else:
            if message.text:
                await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=message.id,
                                              disable_notification=True, schedule_date=date)
            if message.media_group_id:
                media_groups = setting.user_setting[f"{my_id}"]["media_groups"]
                if f"{message.media_group_id}" not in media_groups:
                    media_groups[f"{message.media_group_id}"] = message.id
                    time.sleep(1)
                    ids = []
                    to_add = await client.get_media_group(message.chat.id, media_groups[f"{message.media_group_id}"])
                    for m in to_add:
                        ids.append(m.id)
                    del media_groups[f"{message.media_group_id}"]
                    await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=ids,
                                                  disable_notification=True, schedule_date=date)
            elif message.media:
                if message.video and message.video.ttl_seconds:
                    await self.forward_protected_content_from_chat(message, forward_to, client)
                elif message.photo and message.photo.ttl_seconds:
                    await self.forward_protected_content_from_chat(message, forward_to, client)
                else:
                    await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=message.id,
                                                  disable_notification=True, schedule_date=date)

    @staticmethod
    async def forward_protected_content_from_chat(message, forward_to, client):
        caption = f"Сгораемый файл от пользователя \"{message.from_user.first_name}\", дата и время " \
                  f"сообщения \"{str(message.date)}\"\n{message.caption}"
        file = await client.download_media(message, in_memory=True)
        dt = datetime.now()
        date = dt + timedelta(seconds=cooldown)
        await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                   disable_notification=True, schedule_date=date)

    @staticmethod
    async def forward_protected_content_from_cg(message, forward_to, client, my_id):
        if not message.from_user:
            name = message.chat.title
        elif message.from_user.last_name:
            name = f"{message.from_user.first_name} {message.from_user.last_name}"
        else:
            name = message.from_user.first_name

        if message.media_group_id:
            dt = datetime.now()
            date = dt + timedelta(seconds=cooldown)
            media_groups = setting.user_setting[f"{my_id}"]["media_groups"]
            if f"{message.media_group_id}" not in media_groups:
                media_groups[f"{message.media_group_id}"] = message.id
                time.sleep(1)
                medias = []
                to_add = await client.get_media_group(message.chat.id, media_groups[f"{message.media_group_id}"])
                for m in to_add:
                    file = await client.download_media(m, in_memory=True)
                    caption = ""
                    if m.caption:
                        caption = m.caption
                    docs = InputMediaDocument(media=file, caption=caption)
                    medias.append(docs)
                del media_groups[f"{message.media_group_id}"]
                await client.send_media_group(chat_id=forward_to, media=medias, disable_notification=True,
                                              schedule_date=date)
        elif message.media:
            caption = f"Файл с защищённого канала/группы от пользователя \"{name}\", дата и время " \
                      f"сообщения \"{str(message.date)}\"\n{message.caption}"
            file = await client.download_media(message, in_memory=True)
            dt = datetime.now()
            date = dt + timedelta(seconds=cooldown)
            await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                       disable_notification=True, schedule_date=date)
        elif message.text:
            text = f"Сообщене с защищённого канала/группы от пользователя \"{name}\", дата и " \
                   f"время сообщения \"{str(message.date)}\"\n-----\n{message.text}"
            dt = datetime.now()
            date = dt + timedelta(seconds=cooldown)
            await client.send_message(chat_id=forward_to, text=text, disable_notification=True, schedule_date=date)
