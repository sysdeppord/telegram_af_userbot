from datetime import datetime, timedelta


class Comparator:
    @staticmethod
    def compare_id(chat_id, setting):
        """Method return list of item [forward_to INTEGER, enable INTEGER, forward_self INTEGER]"""
        user_id = chat_id
        for item in setting.forward_setting:
            if item[0] == user_id:
                fs = [item[1], item[2], item[3]]
                return fs


class UserMessages:
    """All forward logic"""

    async def forward_logic(self, client, message, setting):
        comparator = Comparator()
        ft = comparator.compare_id(message.chat.id, setting)
        if not setting.is_pause:
            if ft:
                forward_to = ft[0]
                enable_forwarding = ft[1]
                forward_self = ft[2]
                user_id = message.from_user.id
                my_id = setting.my_id
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
        file = await client.download_media(message)
        print("Downloaded! Trying to send!")
        await client.send_document(chat_id=forward_to, document=file, caption=caption,
                                   disable_notification=True, schedule_date=date)
        print("Sent!")
