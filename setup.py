print("If you don't have api_id, api_hash, bot_token please visit \"https://my.telegram.org/auth?to=apps\" to create "
      "api_id, api_hash, and visit \"https://t.me/botfather\" to create bot_token. Then input those in next dialogs")
api_id = input("Input your API ID: ")
api_hash = input("Input your API HASH: ")
bot_token = input("Input your BOT TOKEN: ")
print("Now input you Telegram id for full admin rights in bot.\nIf you dont know your Telegram id just go to "
      "telegram bot \"https://t.me/my_id_bot\" or another...")
admin_id = input("Input your admin_id: ")

with open('config/tg_config.py', 'r') as f:
    content = f.read()

content = content.replace('api_id = os.environ["api_id"]', f"api_id = {api_id}")
content = content.replace('api_hash = os.environ["api_hash"]', f"api_hash = \"{api_hash}\"")
content = content.replace('bot_token = os.environ["bot_token"]', f"bot_token = \"{bot_token}\"")
content = content.replace('admin_id = int(os.environ["admin_id"])', f"admin_id = \"{admin_id}\"")

with open('config/tg_config.py', 'w') as f:
    f.write(content)

print("DONE!\nIf you need to change some config, just edit file in config/tg_config.py.\nNow just run \"main.py\" "
      "for starting bot :)")
