from pyrogram import Client
from config.tg_config import api_id, api_hash
from proxy_class import setting
from config.app_config import *
import os
import shutil
import datetime

user_apps = {}


class UserAuth:

    @staticmethod
    async def create_app(user_id, phone_number):
        name = f"u{user_id}"
        if not os.path.exists(f"./files/users/{name}"):
            os.mkdir(f"./files/users/{name}")
        app = Client(name, api_id=api_id, api_hash=api_hash, app_version=name_app+ver_app,
                     device_model=device_model, system_version=system_version, workdir=f"./files/users/{name}")
        await app.connect()
        sc = await app.send_code(phone_number=phone_number)
        user_apps[user_id] = {'app': app, 'sc': sc, 'phone_number': phone_number}

    @staticmethod
    async def resend_code(user_id):
        app_data = user_apps[user_id]
        sc = await app_data["app"].send_code(phone_number=app_data['phone_number'])
        app_data['sc'] = sc

    @staticmethod
    async def auth_code(user_id, phone_code, bot):
        if user_id in user_apps:
            app_data = user_apps[user_id]
            pch = app_data['sc'].phone_code_hash
            await app_data['app'].sign_in(phone_number=app_data['phone_number'], phone_code_hash=pch,
                                          phone_code=phone_code)
            info = await app_data['app'].get_me()
            if info.id != user_id:
                setting.user_setting[f"{user_id}"]["temp_data"] = "not_self_id"
                setting.user_setting[f"{user_id}"]["menu_point"] = ""
                tg_info = await bot.get_users(user_id)
                if tg_info.last_name:
                    name = f"{tg_info.first_name} {tg_info.last_name}"
                else:
                    name = tg_info.first_name
                text = f"Произошла попытка несанкционированного входа в твой аккаунт через @CP_forward_bot, " \
                       f"авторизация отклонена!\n\nИнформация о пользователе, который пытался авторизоваться:\n" \
                       f"Имя установленное в телеграм: **[{name}](tg://user?id={user_id})**\n" \
                       f"ID Телеграмм аккаунта: `{user_id}`\n" \
                       f"Юзернейм (если установлен): @{tg_info.username}\n" \
                       f"Время входа: --{datetime.datetime.now()}--"
                await app_data['app'].send_message("me", text)
                await app_data['app'].disconnect()
                shutil.rmtree(f"./files/users/u{user_id}")
            else:
                await app_data['app'].disconnect()

    @staticmethod
    async def check_hint_cloud_password(user_id):
        app_data = user_apps[user_id]
        hint = await app_data['app'].get_password_hint()
        return hint

    @staticmethod
    async def check_cloud_password(user_id, password):
        app_data = user_apps[user_id]
        pwd = await app_data['app'].check_password(password)
        await app_data['app'].disconnect()

    @staticmethod
    async def remove_user_app(user_id):
        del user_apps[user_id]

