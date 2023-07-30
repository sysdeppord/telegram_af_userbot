from pyrogram import Client  # , filters, idle
from config.tg_config import api_id, api_hash
from proxy_class import setting
from config.app_config import *
import os
import shutil
import datetime

apps = []


class UserAuth:

    @staticmethod
    async def create_app(user_id, phone_number):
        name = f"u{user_id}"
        if not os.path.exists(f"./files/users/{name}"):
            os.mkdir(f"./files/users/{name}")
        app = Client(f"{name}", api_id=api_id, api_hash=api_hash, app_version=name_app+ver_app,
                     device_model=device_model, system_version=system_version, workdir=f"./files/users/{name}")
        await app.connect()
        sc = await app.send_code(phone_number=phone_number)
        apps.append([app, sc, phone_number])

    @staticmethod
    async def auth_code(user_id, phone_code, bot):
        for app in apps:
            if app[0].name == f"u{user_id}":
                pch = app[1].phone_code_hash
                await app[0].sign_in(phone_number=app[2], phone_code_hash=pch, phone_code=phone_code)
                info = await app[0].get_me()
                if info.id != user_id:
                    setting.user_setting[f"{user_id}"]["temp_data"] = "not_self_id"
                    setting.user_setting[f"{user_id}"]["menu_point"] = ""
                    tg_info = await bot.get_users(user_id)
                    if tg_info.last_name:
                        name = f"{tg_info.first_name} {tg_info.last_name}"
                    else:
                        name = tg_info.first_name
                    text = f"Произошла попытка несанкцонированого в твой аккаунт входа через @CP_forward_bot, " \
                           f"авторизация отклонена!\n\nИнформация о пользователе, который пытался авторизоваться:\n" \
                           f"Имя установленое в телеграм: **[{name}](tg://user?id={user_id})**\n" \
                           f"ID Телеграмм аккаунта: `{user_id}`\n" \
                           f"Юзернейм (если установлен): @{tg_info.username}\n" \
                           f"Время входа: --{datetime.datetime.now()}--"
                    await app[0].send_message("me", text)
                    await app[0].disconnect()
                    shutil.rmtree(f"./files/users/u{user_id}")

                else:
                    await app[0].disconnect()
