from user_processor import UserMessages


async def user_message(client, message):
    user_processor = UserMessages()
    await user_processor.forward_logic(client, message)
