from datetime import datetime, timedelta
from tg_config import setting


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
                user_id = message.from_user.id
                my_id = int(user)
                if enable_forwarding:
                    if user_id == my_id:
                        if forward_self:
                            await self.forward_processor(message, forward_to, client)
                    else:
                        await self.forward_processor(message, forward_to, client)

    async def forward_processor(self, message, forward_to, client):
        dt = datetime.now()
        date = dt + timedelta(minutes=1)  # This optimal time
        if message.text:
            await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=message.id,
                                          disable_notification=True, schedule_date=date)
        if message.media:
            if message.video and message.video.ttl_seconds:
                await self.forward_protected_content(message, forward_to, client, date)
            elif message.photo and message.photo.ttl_seconds:
                await self.forward_protected_content(message, forward_to, client, date)
            else:
                await client.forward_messages(chat_id=forward_to, from_chat_id=message.chat.id, message_ids=message.id,
                                              disable_notification=True, schedule_date=date)

    @staticmethod
    async def forward_protected_content(message, forward_to, client, date):
        caption = f"Сгораемое ВИДЕО от пользователя \"{message.from_user.first_name}\", дата и время " \
                  f"сообщения \"{str(message.date)}\"\n{message.caption}"
        print("Protected media (burned photo/video), downloading!")
        file = await client.download_media(message, in_memory=True)
        print("Downloaded! Trying to send!")
        await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                   disable_notification=True, schedule_date=date)
        print("Sent!")
