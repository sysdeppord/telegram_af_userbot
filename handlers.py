from user_processor import UserMessages


class UserHandlers:
    def __init__(self, bot_client):
        self.bot_client = bot_client

    async def user_message(self, client, message):
        user_processor = UserMessages()
        await user_processor.forward_logic(client, message, self.bot_client)
