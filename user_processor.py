from datetime import datetime, timedelta
from tg_config import setting

cooldown = 1  # cd for scheduled messages

class UserMessages:
    """All forward logic"""

    async def forward_logic(self, client, message):
        user = client.name.replace("u", "")
        user_setting = setting.user_setting[f"{user}"]
        is_pause = user_setting["pause"]
        if not is_pause:
            if f"{message.chat.id}" in user_setting["forward_setting"]:
                forward_from = user_setting["forward_setting"][f"{message.chat.id}"]
                forward_to = forward_from["forward_to"]
                enable_forwarding = forward_from["enable"]
                forward_self = forward_from["forward_self"]
                user_id = message.chat.id
                my_id = int(user)
                if message.chat.has_protected_content:
                    protected = True
                elif not message.chat.has_protected_content:
                    protected = False
                if enable_forwarding:
                    if user_id == my_id:
                        if forward_self:
                            await self.forward_processor(message, forward_to, client, protected)
                    else:
                        await self.forward_processor(message, forward_to, client, protected)

    async def forward_processor(self, message, forward_to, client, protected):
        dt = datetime.now()
        date = dt + timedelta(minutes=cooldown)
        if protected:
            try:
                await self.forward_protected_content_from_cg(message, forward_to, client)
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
                date = dt + timedelta(minutes=cooldown)
                await client.send_message(chat_id=forward_to, text=text, disable_notification=True, schedule_date=date)
        else:
            if message.text:
                await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=message.id,
                                              disable_notification=True, schedule_date=date)
            if message.media:
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
        date = dt + timedelta(minutes=cooldown)
        await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                   disable_notification=True, schedule_date=date)

    @staticmethod
    async def forward_protected_content_from_cg(message, forward_to, client):
        if not message.from_user:
            name = message.chat.title
        elif message.from_user.last_name:
            name = f"{message.from_user.first_name} {message.from_user.last_name}"
        else:
            name = message.from_user.first_name

        if message.media:
            caption = f"Файл с защищённого канала/группы от пользователя \"{name}\", дата и время " \
                      f"сообщения \"{str(message.date)}\"\n{message.caption}"
            file = await client.download_media(message, in_memory=True)
            dt = datetime.now()
            date = dt + timedelta(minutes=cooldown)
            await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                       disable_notification=True, schedule_date=date)
        if message.text:
            text = f"Сообщене с защищённого канала/группы от пользователя \"{name}\", дата и " \
                   f"время сообщения \"{str(message.date)}\"\n-----\n{message.text}"
            dt = datetime.now()
            date = dt + timedelta(minutes=cooldown)
            await client.send_message(chat_id=forward_to, text=text, disable_notification=True, schedule_date=date)
